import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import interact from 'interactjs';
import html2canvas from 'html2canvas';
import WebFont from 'webfontloader';
import { Type as TypeIcon, Check, Copy } from 'lucide-react'; // Added imports



const GOOGLE_FONTS_API_KEY = 'AIzaSyCVYl_VcBhhzs6n70RqZxikiikabNWCoWc';

const hexToRGBA = (hex, alpha) => {
    if (!hex || hex === 'transparent') return 'transparent';
    try {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    } catch (e) { return 'transparent'; }
};

const toAbsolutePixels = (layer,canvasWidth, canvasHeight) => {
    if (!layer || !layer.bounding_box) return null;
    const { x, y } = layer.bounding_box.min_point;
    return {
        id: layer.text_id,
        text: layer.text_content || "",
        x: (x || 0) * canvasWidth,
        y: (y || 0) * canvasHeight,
        width: ((layer.bounding_box.max_point.x - x) || 0.2) * canvasWidth,
        height: ((layer.bounding_box.max_point.y - y) || 0.1) * canvasHeight,
        fontSize: layer?.element_size || 24,
        fontWeight: 400,
        fontStyle: 'normal',
        textDecoration: 'none',
        color: layer.fill_color?.hex_code || '#000000', 
        fontFamily: layer.font_name || 'Arial',
        backgroundColor: layer.background_color?.hex_code|| '#ffffff', 
        opacity: (layer?.bg_opacity || 0) / 100 
    };
};

export default function App() {
    // 1. Hooks must be inside the component
    const location = useLocation();
    const fullText = location.state?.ad;
    
    const [canvasSize, setCanvasSize] = useState({ width: 800, height: 800 });
    const [layers, setLayers] = useState([]);
    const [allFonts, setAllFonts] = useState([]); 
    const [selectedLayerId, setSelectedLayerId] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [isCopied, setIsCopied] = useState(false);
    const [editedText, setEditedText] = useState(fullText || "");

    useEffect(() => {
    const img = new Image();
    img.src = "http://127.0.0.1:8000/static/image.png";

    img.onload = () => {
        setCanvasSize({
            width: img.naturalWidth,
            height: img.naturalHeight
        });
    };
}, []);
    // Logic for RTL/Arabic detection
    const isArabic = /[\u0600-\u06FF]/.test(editedText);

    const canvasRef = useRef(null);
    const layersRef = useRef(layers);

    useEffect(() => { layersRef.current = layers; }, [layers]);

    // Load fonts when layers change
    useEffect(() => {
        if (layers.length > 0) {
            const activeFonts = [...new Set(layers.map(l => l.fontFamily))];
            WebFont.load({
                google: { families: activeFonts }
            });
        }
    }, [layers]);

    // Initial Data Fetch
    useEffect(() => {
        fetch(`https://www.googleapis.com/webfonts/v1/webfonts?sort=popularity&key=${GOOGLE_FONTS_API_KEY}`)
            .then(res => res.json()).then(data => setAllFonts(data.items || []));
        
        fetch('http://127.0.0.1:8000/static/assets.json')
            .then(res => res.json())
            .then(data => setLayers(data.map (l => toAbsolutePixels(l,canvasSize.width,canvasSize.height))).filter(l => l !== null))
            .catch(err => console.error("JSON Error:", err));
    }, []);

    const updateLayer = useCallback((id, updates) => {
        if (!id) return;
        setLayers(prev => prev.map(l => l.id === id ? { ...l, ...updates } : l));
    }, []);

    const handleCopyText = () => {
        navigator.clipboard.writeText(editedText);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
    };

    // InteractJS Setup
    useEffect(() => {
        if (layers.length === 0) return;
        const instance = interact('.draggable').draggable({
            listeners: {
                move(event) {
                    const id = parseInt(event.target.dataset.id);
                    const layer = layersRef.current.find(l => l.id === id);
                    if (layer) updateLayer(id, { x: layer.x + event.dx, y: layer.y + event.dy });
                }
            }
        }).resizable({
            edges: { left: true, right: true, bottom: true, top: true },
            listeners: {
                move(event) {
                    const id = parseInt(event.target.dataset.id);
                    const layer = layersRef.current.find(l => l.id === id);
                    if (layer) {
                        updateLayer(id, {
                            x: layer.x + event.deltaRect.left,
                            y: layer.y + event.deltaRect.top,
                            width: event.rect.width,
                            height: event.rect.height
                        });
                    }
                }
            }
        });
        return () => instance.unset();
    }, [layers.length, updateLayer]);

    const selectedLayer = layers.find(l => l.id === selectedLayerId);

    return (
        <div id="app-viewport">
            <div className="editor-main">
                <aside className="sidebar left-sidebar">
                    <div className="inspector">
                        <div className={`flex items-center gap-2 mb-4 text-indigo-600 ${isArabic ? 'flex-row-reverse' : 'flex-row'}`}>
                             <TypeIcon className="w-5 h-5" />
                             <span className="text-xs font-black uppercase tracking-widest">Post Copy Editor</span>
                        </div>
                        <h3>Social Media Post</h3>
                        <div className="post-preview-container">
                            <label>Caption Preview</label>
                            <div className="social-post-text">
                                <textarea 
                                    className={`w-full p-0 bg-transparent outline-none min-h-[350px] text-gray-900 text-2xl font-medium leading-relaxed transition-all resize-none font-trirong focus:ring-0 border-none ${isArabic ? 'text-right' : 'text-left'}`}                                    value={editedText}
                                    onChange={(e) => setEditedText(e.target.value)}
                                    spellCheck="false"
                                    dir="auto"
                                />
                                <button 
                                    onClick={handleCopyText} 
                                    className={`flex items-center justify-center gap-3 w-full py-3 rounded-xl font-bold transition-all active:scale-95 border-2 ${
                                      isCopied 
                                        ? 'bg-green-50 border-green-500 text-green-600' 
                                        : 'bg-white border-indigo-600 text-indigo-600 hover:bg-indigo-50'
                                    }`}
                                  >
                                    {isCopied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                                    {isCopied ? 'Copied' : 'Copy Text'}
                                </button>
                                <button className="btn-export" onClick={async () => {
    // 1. Store the current selection
    const currentSelection = selectedLayerId;
    
    // 2. Deselect the layer so the border disappears
    setSelectedLayerId(null);

    // 3. Wait for one "tick" to allow React to remove the 'active' class from the DOM
    setTimeout(async () => {
        const canvas = await html2canvas(canvasRef.current, { 
            useCORS: true, 
            scale: 2,
            backgroundColor: null // Ensures transparency is preserved if needed
        });
        
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = 'export.png';
        link.click();

        // 4. Restore the selection so the user can keep editing
        setSelectedLayerId(currentSelection);
    }, 0);
}}>
    Export PNG
</button>
                            </div>
                        </div>
                    </div>
                </aside>

                <section className="stage">
                    <div
                        ref={canvasRef}
                        className="canvas"
                        style={{
                            width: canvasSize.width,
                            height: canvasSize.height,
                            backgroundImage: "url('http://127.0.0.1:8000/static/image.png')",
                            backgroundSize: "cover",
                            backgroundPosition: "center",
                            position: "relative",
                            overflow: "auto",
                            backgroundColor: "#ffffff"
                        }}
                    >
                        {layers.map(layer => (
                            <div key={layer.id} data-id={layer.id} 
                                className={`draggable ${selectedLayerId === layer.id ? 'active' : ''}`}
                                style={{
                                    position: 'absolute',
                                    left: 0,
                                    top: 0,
                                    transform: `translate(${layer.x}px, ${layer.y}px)`,
                                    fontSize: `${layer.fontSize}px`, 
                                    fontWeight: layer.fontWeight,
                                    fontStyle: layer.fontStyle,
                                    textDecoration: layer.textDecoration,
                                    color: layer.color, 
                                    fontFamily: layer.fontFamily,
                                    width: `${layer.width}px`, 
                                    height: `${layer.height}px`,
                                    backgroundColor: hexToRGBA(layer.backgroundColor, layer.opacity),
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    justifyContent: 'center', 
                                    textAlign: 'center', 
                                    direction: 'rtl',
                                    cursor: 'move',
                                    border: selectedLayerId === layer.id ? '2px solid #6366f1' : '1px transparent'
                                }}
                                onClick={(e) => { e.stopPropagation(); setSelectedLayerId(layer.id); setIsDropdownOpen(false); }}>
                                {layer.text}
                            </div>
                        ))}
                    </div>
                </section>

                <aside className="sidebar">
                    {selectedLayer ? (
                        <div className="inspector">
                            <h3>Properties</h3>
                            <label>Text Content</label>
                            <textarea value={selectedLayer.text} onChange={(e) => updateLayer(selectedLayerId, { text: e.target.value })} />

                            <label>Toolbar</label>
                            <div className="word-toolbar">
                                <button className={selectedLayer.fontWeight >= 700 ? 'on' : ''} onClick={() => updateLayer(selectedLayerId, { fontWeight: selectedLayer.fontWeight >= 700 ? 400 : 700 })}>B</button>
                                <button className={selectedLayer.fontStyle === 'italic' ? 'on' : ''} onClick={() => updateLayer(selectedLayerId, { fontStyle: selectedLayer.fontStyle === 'italic' ? 'normal' : 'italic' })}>I</button>
                                <button className={selectedLayer.textDecoration === 'underline' ? 'on' : ''} onClick={() => updateLayer(selectedLayerId, { textDecoration: selectedLayer.textDecoration === 'underline' ? 'none' : 'underline' })}>U</button>
                                
                                <div className="color-tool">
                                    <span className="icon">A</span>
                                    <div className="bar" style={{ background: selectedLayer.color }}></div>
                                    <input type="color" value={selectedLayer.color} onChange={(e) => updateLayer(selectedLayerId, { color: e.target.value })} />
                                </div>

                                <div className="color-tool">
                                    <span className="icon sm">ab</span>
                                    <div className="bar" style={{ background: selectedLayer.backgroundColor }}></div>
                                    <input type="color" value={selectedLayer.backgroundColor} onChange={(e) => updateLayer(selectedLayerId, { backgroundColor: e.target.value })} />
                                </div>
                            </div>

                            <div className="split-row">
                                <div className="col">
                                    <label>Size (px)</label>
                                    <input type="number" value={selectedLayer.fontSize} onChange={(e) => updateLayer(selectedLayerId, { fontSize: parseInt(e.target.value) || 12 })} />
                                </div>
                                <div className="col">
                                    <label>Opacity ({Math.round(selectedLayer.opacity * 100)}%)</label>
                                    <input type="range" min="0" max="1" step="0.01" value={selectedLayer.opacity} onChange={(e) => updateLayer(selectedLayerId, { opacity: parseFloat(e.target.value) })} />
                                </div>
                            </div>

                            <label>Font Family</label>
                            <div className="font-dropdown">
                                <div className="dropdown-head" onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
                                    {selectedLayer.fontFamily} <span>▼</span>
                                </div>
                                {isDropdownOpen && (
                                    <div className="dropdown-body">
                                        <input type="text" placeholder="Search fonts..." autoFocus value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
                                        <div className="scroll-box">
                                            {allFonts.filter(f => f.family.toLowerCase().includes(searchTerm.toLowerCase())).slice(0, 50).map(f => (
                                                <div key={f.family} onClick={() => { updateLayer(selectedLayerId, { fontFamily: f.family }); setIsDropdownOpen(false); }}>{f.family}</div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    ) : <div className="empty-state">Select a text layer</div>}
                </aside>
            </div>
        <style>
               {
                `:root {
    --bg-dark: #ffffff;
    --bg-side: #f4f5f7;
    --accent: #3b82f6;
    --border: #d1d5db;
    --text-muted: #6b7280;
}

* { box-sizing: border-box; }

body { 
    margin: 0; 
    font-family: 'Inter', sans-serif; 
    background: #ffffff; 
    color: #111827; 
    overflow: auto; 
    width: 100vw;
}

#app-viewport { display: flex; flex-direction: column; height: 100vh; }

.navbar {
    height: 56px; background: var(--bg-side); border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between; padding: 0 20px; flex-shrink: 0;
}

.logo { font-weight: 800; font-size: 18px; }
.logo span { color: var(--accent); }

.btn-export { background: var(--accent); border: none; color: white; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; }

.editor-main { display: flex; flex: 1; overflow: auto; }

.stage {
    flex: 1; 
    background: #f3f4f6ff;
     display: flex; 
     align-items: center; 
     justify-content: center; 
     overflow: auto;
}

.canvas { background-size: cover; 
background-position: center; 
position: relative; 
box-shadow: 0 20px 60px rgba(0,0,0,0.6);
 flex-shrink: 0;
  background-color: white; }

.sidebar {
    width: 360px;
    background: #ffffff;
    border-left: 1px solid var(--border);
    padding: 24px;
    flex-shrink: 0;
    overflow-y: auto;
}


.inspector h3 { margin: 0 0 20px 0; font-size: 16px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
label { display: block; font-size: 10px; color: var(--text-muted); text-transform: uppercase; margin-top: 15px; margin-bottom: 6px; font-weight: 800; }

textarea {
    width: 100%; height: 60px; background: #f3f4f6ff; border: 1px solid var(--border); color: black; padding: 10px; border-radius: 6px; resize: none;
    

}


.split-row { display: flex; gap: 12px; margin-top: 5px; }
.col { flex: 1; }

input[type="number"] {
    width: 100%; background: #ffffffff; border: 1px solid var(--border); color: black; padding: 10px; border-radius: 6px;
}

/* Restored Opacity Scroller Style */
input[type="range"] {
    width: 100%; height: 6px; background: #f3f4f6ff; border-radius: 5px; appearance: none; outline: none; margin-top: 12px;
}
input[type="range"]::-webkit-slider-thumb {
    appearance: none; width: 14px; height: 14px; background: var(--accent); border-radius: 50%; cursor: pointer;
}

.word-toolbar {
    display: flex; gap: 4px; background: #f3f4f6ff; padding: 4px; border-radius: 6px; border: 1px solid var(--border);
}

.word-toolbar button {
    flex: 1; height: 36px; background: none; border: none; color: black; cursor: pointer; border-radius: 4px; font-weight: bold;
}

.word-toolbar button.on { background: var(--accent); }

.color-tool { position: relative; flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.color-tool .icon { font-size: 14px; font-weight: 800; }
.color-tool .icon.sm { font-size: 10px; }
.color-tool .bar { width: 20px; height: 3px; position: absolute; bottom: 4px; border-radius: 1px; }
.color-tool input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }

.font-dropdown { position: relative; }
.dropdown-head { background: #f3f4f6ff; padding: 12px; border-radius: 6px; border: 1px solid var(--border); cursor: pointer; display: flex; justify-content: space-between; font-size: 13px; }
.dropdown-body { position: absolute; bottom: 100%; left: 0; right: 0; background: #f3f4f6ff; border: 1px solid var(--border); border-radius: 8px; padding: 10px; z-index: 100; margin-bottom: 5px; box-shadow: 0 -10px 20px rgba(0,0,0,0.5); }
.dropdown-body input { width: 100%; background: #f3f4f6ff; border: 1px solid var(--border); padding: 8px; color: black; border-radius: 4px; margin-bottom: 8px; }
.scroll-box { max-height: 200px; overflow-y: auto; }
.scroll-box div { padding: 8px; cursor: pointer; font-size: 13px; }
.scroll-box div:hover { background: var(--accent); }

.draggable { position: absolute; cursor: move; }
.draggable.active { outline: 2px solid var(--accent); outline-offset: 4px; }
.empty-state { text-align: center; color: #555; margin-top: 100px; }
/* Update or add these rules in App.css */

.sidebar.left-sidebar textarea {
    height: 80%;
    min-height: 260px;
    resize: vertical;
    overflow-y: auto;
    background: #ffffff;
    color: #111827;
    font-size: 16px;
    line-height: 1.6;
}


.social-post-text {
    background: #ffffff;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border);
    font-size: 14px;
    line-height: 1.6;
    color: #111827;
    white-space: pre-wrap;
    height : 90%
    
}

.post-preview-container {
    height : 90%;
}
.inspector {
height : 95%;
}

@keyframes fade-in { 
    from { opacity: 0; transform: translateY(20px); } 
    to { opacity: 1; transform: translateY(0); } 
}

.animate-fade-in { 
    animation: fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; 
}

@keyframes shake { 
    0%, 100% { transform: translateX(0); } 
    20% { transform: translateX(-8px); } 
    40% { transform: translateX(8px); } 
    60% { transform: translateX(-4px); } 
    80% { transform: translateX(4px); } 
}

.animate-shake { 
    animation: shake 0.4s ease-in-out; 
}

/* Scrollbar Customization */
.custom-scrollbar::-webkit-scrollbar { 
    width: 4px; 
}

.custom-scrollbar::-webkit-scrollbar-track { 
    background: transparent; 
}

.custom-scrollbar::-webkit-scrollbar-thumb { 
    background: #e2e8f0; 
    border-radius: 10px; 
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover { 
    background: #cbd5e1; 
}
`
               }     
        </style>
        </div>
        
    );
}