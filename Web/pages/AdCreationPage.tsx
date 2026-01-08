
import React, { useState, useMemo } from 'react';
import { Sparkles, Download, ArrowLeft, RefreshCw, Type as TypeIcon, Image as ImageIcon, Copy, Check, LayoutGrid, Settings2, Plus, X, Users, Globe, Target, ShieldAlert, MousePointer2, Info } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { generateAd } from '../services/apiService';
import { AdContent, AppStatus, AdvancedInput, BackendAdRequest} from '../types';


// Moved outside to ensure stable component reference and prevent focus loss during typing
const FormField = ({ label, icon: Icon, children }: { label: string, icon?: any, children: React.ReactNode }) => (
  <div className="flex flex-col gap-2">
    <label className="text-[11px] font-bold text-gray-400 uppercase tracking-widest flex items-center gap-1.5 ml-1">
      {Icon && <Icon className="w-3 h-3 text-indigo-500" />}
      {label}
    </label>
    {children}
  </div>
);

const AdCreationPage: React.FC = () => {
  const navigate = useNavigate()
  const [inputType, setInputType] = useState<'basic' | 'advanced'>('basic');
  const [basicDescription, setBasicDescription] = useState('');
  
  // Advanced State
  const [advancedData, setAdvancedData] = useState<AdvancedInput>({
    mainPrompt: '',
    brandName: '',
    productName: '',
    brandLogo: undefined,
    productReferenceImages: [],
    humanModelImages: [],
    artisticStyle: '',
    aspectRatio: '1:1',
    location: '',
    language: 'English',
    negativeConstraints: '',
    targetAudience: '',
    callToAction: '',
    additionalInfo: ''
  });

  const [status, setStatus] = useState<AppStatus>(AppStatus.IDLE);
  const [ad, setAd] = useState<AdContent | null>(null);
  const [isCopied, setIsCopied] = useState(false);
  const [editedText, setEditedText] = useState('');

  const isArabic = useMemo(() => {
    const arabicPattern = /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]/;
    return arabicPattern.test(editedText);
  }, [editedText]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'logo' | 'product' | 'human') => {
    const files = e.target.files;
    if (!files) return;

    (Array.from(files) as File[]).forEach(file => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result as string;
        if (type === 'logo') setAdvancedData(prev => ({ ...prev, brandLogo: base64 }));
        if (type === 'product') setAdvancedData(prev => ({ ...prev, productReferenceImages: [...prev.productReferenceImages, base64].slice(0, 3) }));
        if (type === 'human') setAdvancedData(prev => ({ ...prev, humanModelImages: [...prev.humanModelImages, base64].slice(0, 3) }));
      };
      reader.readAsDataURL(file);
    });
  };

  const removeImage = (type: 'logo' | 'product' | 'human', index?: number) => {
    if (type === 'logo') setAdvancedData(prev => ({ ...prev, brandLogo: undefined }));
    if (type === 'product' && index !== undefined) setAdvancedData(prev => ({ ...prev, productReferenceImages: prev.productReferenceImages.filter((_, i) => i !== index) }));
    if (type === 'human' && index !== undefined) setAdvancedData(prev => ({ ...prev, humanModelImages: prev.humanModelImages.filter((_, i) => i !== index) }));
  };
  const mapBasicToBackend = (text: string) => ({
  main_prompt: text,
  info_type: "basic" as const
});
const mapAdvancedToBackend = (data: AdvancedInput) => ({
  main_prompt: data.mainPrompt,
  info_type: "advanced" as const,
  brand_name: data.brandName || '',
  product_name: data.productName || '',
  brand_logo: data.brandLogo || '',
  product_reference_images: data.productReferenceImages || [],
  human_model_images: data.humanModelImages || [],
  artistic_style: data.artisticStyle || '',
  aspect_ratio: data.aspectRatio,
  location: data.location || '',
  language: data.language || '',
  negative_constraints: data.negativeConstraints || '',
  target_audience: data.targetAudience || '',
  call_to_action: data.callToAction || '',
  additional_information: data.additionalInfo || ''
});



const handleGenerate = async () => {
  if (inputType === 'basic' && !basicDescription.trim()) return;
  if (inputType === 'advanced' && !advancedData.mainPrompt.trim()) return;

  setStatus(AppStatus.LOADING);
  setIsCopied(false);

  try {
    const payload =
      inputType === 'basic'
        ? mapBasicToBackend(basicDescription)
        : mapAdvancedToBackend(advancedData);

    const result = await generateAd(payload);
    setAd(result);

    const fullText = `${result.headline}\n\n${result.body}\n\n${result.hashtags
      .map(tag => (tag.startsWith('#') ? tag : `#${tag}`))
      .join(' ')}`;
      navigate('/result', { state: { ad: fullText } });

    setEditedText(fullText);
    setStatus(AppStatus.SUCCESS);
  } catch (error) {
    console.error(error);
    setStatus(AppStatus.ERROR);
  }
};

  

  const handleCopyText = async () => {
    try {
      await navigator.clipboard.writeText(editedText);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleDownloadImage = () => {
    if (!ad?.imageUrl) return;
    const imageLink = document.createElement('a');
    imageLink.href = ad.imageUrl;
    imageLink.download = 'e3lanak-ai-ad.png';
    document.body.appendChild(imageLink);
    imageLink.click();
    document.body.removeChild(imageLink);
  };

  const inputBaseStyle = "w-full px-4 py-3.5 border border-gray-100 rounded-2xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all bg-white text-gray-700 shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)]";

  return (
    <div className="min-h-screen bg-gray-50/50 pb-20 font-inter">
      <div className="max-w-7xl mx-auto px-4 pt-10">

        {/* Toggle Controls */}
        <div className="flex justify-center mb-12">
          <div className="bg-white p-2 rounded-[24px] shadow-sm border border-gray-100 flex gap-2">
            <button
              onClick={() => { setInputType('basic'); setStatus(AppStatus.IDLE); setAd(null); }}
              className={`flex items-center gap-2 px-8 py-3.5 rounded-[18px] font-bold transition-all ${
                inputType === 'basic' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'text-gray-400 hover:text-indigo-600 hover:bg-indigo-50/50'
              }`}
            >
              <LayoutGrid className="w-5 h-5" />
              Basic Mode
            </button>
            <button
              onClick={() => { setInputType('advanced'); setStatus(AppStatus.IDLE); setAd(null); }}
              className={`flex items-center gap-2 px-8 py-3.5 rounded-[18px] font-bold transition-all ${
                inputType === 'advanced' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'text-gray-400 hover:text-indigo-600 hover:bg-indigo-50/50'
              }`}
            >
              <Settings2 className="w-5 h-5" />
              Advanced Pro
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start">
          {/* Input Panel */}
          <div className="bg-white p-10 rounded-[40px] shadow-[0_20px_50px_-20px_rgba(0,0,0,0.08)] border border-gray-50">
            <div className="flex items-center justify-between mb-10">
              <h1 className="text-2xl font-black text-gray-900 flex items-center gap-3">
                <div className="bg-indigo-50 p-2.5 rounded-2xl">
                  <Sparkles className="text-indigo-600 w-6 h-6" />
                </div>
                {inputType === 'basic' ? 'Instant Ad Generator' : 'Campaign Studio'}
              </h1>
              <span className="text-[10px] font-bold text-indigo-500 bg-indigo-50 px-3 py-1 rounded-full uppercase tracking-tighter">Powered by Gemini 3</span>
            </div>

            {inputType === 'basic' ? (
              <div className="space-y-6 animate-fade-in">
                <FormField label="Describe your ad goal" icon={TypeIcon}>
                  <textarea
                    className={`${inputBaseStyle} min-h-[350px] resize-none text-lg leading-relaxed`}
                    placeholder="Example: I want to promote my new organic skincare brand for young adults. Focus on glowing skin and eco-friendly packaging..."
                    value={basicDescription}
                    onChange={(e) => setBasicDescription(e.target.value)}
                  />
                </FormField>
              </div>
            ) : (
              <div className="space-y-8 animate-fade-in max-h-[75vh] overflow-y-auto pr-4 custom-scrollbar scroll-smooth">
                {/* 1. The Big Prompt */}
                <FormField label="Main Creative Prompt" icon={Sparkles}>
                  <textarea
                    className={`${inputBaseStyle} min-h-[160px] resize-none text-md`}
                    placeholder="Detail the core creative idea, mood, and specific scene details for the AI..."
                    value={advancedData.mainPrompt}
                    onChange={(e) => setAdvancedData({ ...advancedData, mainPrompt: e.target.value })}
                  />
                </FormField>

                {/* 2. Brand & Product Names */}
                <div className="grid grid-cols-2 gap-5">
                  <FormField label="Brand Name">
                    <input
                      className={inputBaseStyle}
                      placeholder="e.g. Luminara"
                      value={advancedData.brandName}
                      onChange={(e) => setAdvancedData({ ...advancedData, brandName: e.target.value })}
                    />
                  </FormField>
                  <FormField label="Product Name">
                    <input
                      className={inputBaseStyle}
                      placeholder="e.g. Hydra Glow Serum"
                      value={advancedData.productName}
                      onChange={(e) => setAdvancedData({ ...advancedData, productName: e.target.value })}
                    />
                  </FormField>
                </div>

                {/* 3. Assets Selection */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField label="Brand Logo" icon={ImageIcon}>
                    <div className="relative group aspect-video border-2 border-dashed border-gray-100 rounded-2xl flex items-center justify-center overflow-hidden bg-white hover:border-indigo-300 transition-all shadow-sm">
                      {advancedData.brandLogo ? (
                        <>
                          <img src={advancedData.brandLogo} className="w-full h-full object-contain p-4" alt="Logo" />
                          <button onClick={() => removeImage('logo')} className="absolute top-2 right-2 bg-white/90 p-1.5 rounded-full text-red-500 opacity-0 group-hover:opacity-100 transition-all shadow-sm hover:scale-110"><X size={16}/></button>
                        </>
                      ) : (
                        <label className="cursor-pointer flex flex-col items-center p-6 text-center group">
                          <Plus className="text-gray-300 w-8 h-8 mb-2 group-hover:text-indigo-400 group-hover:scale-110 transition-all" />
                          <span className="text-[10px] text-gray-400 font-bold uppercase">Click to Upload</span>
                          <input type="file" className="hidden" accept="image/*" onChange={(e) => handleFileUpload(e, 'logo')} />
                        </label>
                      )}
                    </div>
                  </FormField>

                  <FormField label="Product References (Up to 3)" icon={ImageIcon}>
                    <div className="grid grid-cols-3 gap-2 h-full min-h-[100px]">
                      {advancedData.productReferenceImages.map((img, i) => (
                        <div key={i} className="relative group aspect-square border border-gray-100 rounded-xl overflow-hidden bg-white shadow-sm">
                          <img src={img} className="w-full h-full object-cover" alt={`Ref ${i}`} />
                          <button onClick={() => removeImage('product', i)} className="absolute top-1 right-1 bg-white/90 p-1 rounded-full text-red-500 opacity-0 group-hover:opacity-100 shadow-sm"><X size={12}/></button>
                        </div>
                      ))}
                      {advancedData.productReferenceImages.length < 3 && (
                        <label className="cursor-pointer aspect-square border-2 border-dashed border-gray-100 rounded-xl flex items-center justify-center bg-white hover:border-indigo-300 transition-all">
                           <Plus className="text-gray-300" />
                           <input type="file" className="hidden" multiple accept="image/*" onChange={(e) => handleFileUpload(e, 'product')} />
                        </label>
                      )}
                    </div>
                  </FormField>
                </div>

                <FormField label="Human Model References" icon={Users}>
                  <div className="grid grid-cols-4 gap-3">
                    {advancedData.humanModelImages.map((img, i) => (
                      <div key={i} className="relative group aspect-square border border-gray-100 rounded-xl overflow-hidden bg-white shadow-sm">
                        <img src={img} className="w-full h-full object-cover" alt={`Model ${i}`} />
                        <button onClick={() => removeImage('human', i)} className="absolute top-1 right-1 bg-white/90 p-1 rounded-full text-red-500 opacity-0 group-hover:opacity-100 shadow-sm"><X size={12}/></button>
                      </div>
                    ))}
                    {advancedData.humanModelImages.length < 4 && (
                      <label className="cursor-pointer aspect-square border-2 border-dashed border-gray-100 rounded-xl flex items-center justify-center bg-white hover:border-indigo-300 transition-all">
                        <Plus className="text-gray-300" />
                        <input type="file" className="hidden" multiple accept="image/*" onChange={(e) => handleFileUpload(e, 'human')} />
                      </label>
                    )}
                  </div>
                </FormField>

                {/* 4. Artistic Settings */}
                <div className="grid grid-cols-2 gap-5">
                  <FormField label="Artistic Style">
                    <input className={inputBaseStyle} placeholder="e.g. Cartoon, Ultrarealistic" value={advancedData.artisticStyle} onChange={(e) => setAdvancedData({ ...advancedData, artisticStyle: e.target.value })} />
                  </FormField>
                  <FormField label="Aspect Ratio">
                    <select
                      className={inputBaseStyle}
                      value={advancedData.aspectRatio}
                      onChange={(e) => setAdvancedData({ ...advancedData, aspectRatio: e.target.value as any })}
                    >
                      <option value="1:1">1:1 Square (Instagram)</option>
                      <option value="9:16">9:16 Vertical (Story/TikTok)</option>
                      <option value="16:9">16:9 Landscape (Ads)</option>
                      <option value="4:3">4:3 Standard</option>
                      <option value="2:3">2:3</option>
                      <option value="3:2">3:2</option>
                      <option value="3:4">3:4</option>
                      <option value="4:5">4:5</option>
                      <option value="5:4">5:4</option>
                      <option value="21:9">21:9</option> 
                    </select>
                  </FormField>
                </div>

                <div className="grid grid-cols-2 gap-5">
                  <FormField label="Location / Scene" icon={ImageIcon}>
                    <input className={inputBaseStyle} placeholder="e.g. Modern Studio, Beach" value={advancedData.location} onChange={(e) => setAdvancedData({ ...advancedData, location: e.target.value })} />
                  </FormField>
                  <FormField label="Target Language" icon={Globe}>
                    <input className={inputBaseStyle} placeholder="e.g. Arabic, French" value={advancedData.language} onChange={(e) => setAdvancedData({ ...advancedData, language: e.target.value })} />
                  </FormField>
                </div>

                {/* 5. Strategy Meta */}
                <FormField label="Target Audience" icon={Target}>
                  <input className={inputBaseStyle} placeholder="e.g. Health-conscious moms 30-45" value={advancedData.targetAudience} onChange={(e) => setAdvancedData({ ...advancedData, targetAudience: e.target.value })} />
                </FormField>
                
                <FormField label="Call to Action" icon={MousePointer2}>
                  <input className={inputBaseStyle} placeholder="e.g. Buy Now for 50% Off" value={advancedData.callToAction} onChange={(e) => setAdvancedData({ ...advancedData, callToAction: e.target.value })} />
                </FormField>

                <FormField label="Negative Constraints" icon={ShieldAlert}>
                  <input className={inputBaseStyle} placeholder="Avoid these (e.g. text in image, blur)" value={advancedData.negativeConstraints} onChange={(e) => setAdvancedData({ ...advancedData, negativeConstraints: e.target.value })} />
                </FormField>

                <FormField label="Additional Information" icon={Info}>
                  <textarea
                    className={`${inputBaseStyle} min-h-[140px] resize-none text-md`}
                    placeholder="Specific product benefits, current offers, or legal disclaimers..."
                    value={advancedData.additionalInfo}
                    onChange={(e) => setAdvancedData({ ...advancedData, additionalInfo: e.target.value })}
                  />
                </FormField>
              </div>
            )}

            <button
              onClick={handleGenerate}
              
              disabled={status === AppStatus.LOADING}
              className={`w-full mt-12 py-5 rounded-[24px] font-black text-xl flex items-center justify-center gap-3 transition-all shadow-xl active:scale-95 ${
                status === AppStatus.LOADING 
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed' 
                  : 'bg-indigo-600 text-white hover:bg-indigo-700 hover:shadow-indigo-500/40'
              }`}
            >
              {status === AppStatus.LOADING ? (
                <RefreshCw className="animate-spin w-7 h-7" />
              ) : (
                <>
                  <Sparkles className="w-7 h-7" />
                  Generate My Ad
                </>
              )}
              
            </button>
          </div>

          {/* Result Panel */}
          <div className="space-y-8 lg:sticky lg:top-24">
            <h2 className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] flex items-center gap-2 px-1">
              <ImageIcon className="w-4 h-4 text-indigo-400" />
              Creative Preview
            </h2>
            
            {(status === AppStatus.IDLE || status === AppStatus.LOADING) && (
              <div className="aspect-[4/5] bg-white border-2 border-dashed border-gray-100 rounded-[40px] flex flex-col items-center justify-center text-center p-12 relative overflow-hidden shadow-inner group">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/20 to-transparent opacity-50 pointer-events-none" />
                {status === AppStatus.LOADING ? (
                  <div className="flex flex-col items-center animate-pulse">
                    <div className="relative mb-8">
                      <div className="w-24 h-24 border-[6px] border-indigo-50 border-t-indigo-600 rounded-full animate-spin" />
                      <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 text-indigo-600" />
                    </div>
                    <p className="text-2xl font-black text-gray-900 mb-2">Generating Vision...</p>
                    <p className="text-gray-400 font-medium max-w-xs">AI is painting your custom visual and drafting high-conversion copy.</p>
                  </div>
                ) : (
                  <>
                    <div className="w-20 h-20 bg-gray-50 rounded-[28px] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                       <ImageIcon className="w-10 h-10 text-indigo-100" />
                    </div>
                    <p className="text-gray-400 font-bold text-lg">Your masterpiece awaits</p>
                    <p className="text-gray-300 text-sm mt-2">Enter your details and click Generate</p>
                  </>
                )}
              </div>
            )}



            {ad && status === AppStatus.SUCCESS && (
              
              <div className="space-y-8 animate-fade-in">
                <div className="bg-white rounded-[40px] shadow-[0_30px_60px_-15px_rgba(0,0,0,0.12)] border border-gray-100 overflow-hidden ring-1 ring-black/5">
                  <div className="relative">
                    <img src={ad.imageUrl} alt="Result" className="w-full h-auto object-cover max-h-[650px]" />
                    <div className="absolute top-6 left-6 bg-indigo-600/90 backdrop-blur-md text-white px-4 py-2 rounded-full text-[10px] font-black uppercase tracking-widest shadow-xl">
                      {inputType.toUpperCase()} GENERATION
                    </div>
                  </div>

                  <div className="p-10 bg-white">
                    <div className={`flex items-center gap-2 mb-8 text-indigo-600 ${isArabic ? 'flex-row-reverse' : 'flex-row'}`}>
                      <TypeIcon className="w-6 h-6" />
                      <span className="text-xs font-black uppercase tracking-widest">Post Copy Editor</span>
                    </div>
                    <textarea 
                      className={`w-full p-0 bg-transparent outline-none min-h-[350px] text-gray-900 text-2xl font-medium leading-relaxed transition-all resize-none font-trirong focus:ring-0 border-none ${isArabic ? 'text-right' : 'text-left'}`}
                      value={editedText}
                      onChange={(e) => setEditedText(e.target.value)}
                      spellCheck="false"
                      dir="auto"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <button 
                    onClick={handleCopyText} 
                    className={`flex items-center justify-center gap-3 py-5 rounded-[24px] font-black text-lg shadow-xl transition-all active:scale-95 border-2 ${
                      isCopied 
                        ? 'bg-green-50 border-green-500 text-green-600' 
                        : 'bg-white border-indigo-600 text-indigo-600 hover:bg-indigo-50'
                    }`}
                  >
                    {isCopied ? <Check className="w-6 h-6" /> : <Copy className="w-6 h-6" />}
                    {isCopied ? 'Copied' : 'Copy Text'}
                  </button>
                  <button 
                    onClick={handleDownloadImage} 
                    className="flex items-center justify-center gap-3 bg-indigo-600 text-white py-5 rounded-[24px] font-black text-lg shadow-xl hover:bg-indigo-700 transition-all active:scale-95 border-2 border-indigo-600"
                  >
                    <Download className="w-6 h-6" />
                    Save Visual
                  </button>
                </div>
              </div>
            )}

            {status === AppStatus.ERROR && (
              <div className="bg-red-50 border border-red-100 rounded-[40px] p-12 text-center shadow-xl animate-shake">
                <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <X className="text-red-500 w-10 h-10" />
                </div>
                <h3 className="text-2xl font-black text-gray-900 mb-3">Something Went Wrong</h3>
                <p className="text-red-500/80 font-medium mb-8">We couldn't connect to our creative engine. Please try again.</p>
                <button 
                  onClick={handleGenerate}
                  className="bg-red-500 text-white px-10 py-4 rounded-2xl font-black hover:bg-red-600 transition-colors shadow-lg shadow-red-200"
                >
                  Retry Generation
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      <style>{`
        @keyframes fade-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fade-in { animation: fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        
        @keyframes shake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-8px); } 40% { transform: translateX(8px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); } }
        .animate-shake { animation: shake 0.4s ease-in-out; }

        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }
      `}</style>
    </div>
  );
};

export default AdCreationPage;
