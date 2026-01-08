
import { GoogleGenAI, Type } from "@google/genai";
import { AdContent, AdvancedInput } from "../types";

// Always use the API_KEY directly from process.env as per guidelines
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

/**
 * Generates both text and image for an advertisement post.
 * Supports basic string input or complex AdvancedInput object.
 */
export const generateAd = async (input: string | AdvancedInput): Promise<AdContent> => {
  const isAdvanced = typeof input !== 'string';
  
  // 1. Construct the Text Prompt
  let textPrompt = "";
  let language = "English";
  
  if (isAdvanced) {
    const adv = input as AdvancedInput;
    language = adv.language || "English";
    textPrompt = `Write a professional social media ad for ${adv.brandName}'s ${adv.productName}. 
    Core Message: ${adv.mainPrompt}
    Target Audience: ${adv.targetAudience}
    Call to Action: ${adv.callToAction}
    Language: ${language}
    Additional Info: ${adv.additionalInfo}
    Negative Constraints (avoid these): ${adv.negativeConstraints}
    Format as JSON with headline, body, and 3-5 hashtags.`;
  } else {
    textPrompt = `Write a professional social media ad for: "${input}". Format as JSON with headline, body, and 3-5 hashtags.`;
  }

  // Generate Ad Copy (Text)
  const textResponse = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: textPrompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          headline: { type: Type.STRING },
          body: { type: Type.STRING },
          hashtags: {
            type: Type.ARRAY,
            items: { type: Type.STRING }
          }
        },
        required: ["headline", "body", "hashtags"]
      }
    }
  });

  // Access .text property directly as it's a getter in GenerateContentResponse
  const adCopy = JSON.parse(textResponse.text || '{}');

  // 2. Generate Ad Image
  let imagePrompt = "";
  let imageParts: any[] = [];
  let aspectRatio: "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9";

  if (isAdvanced) {
    const adv = input as AdvancedInput;
    aspectRatio = adv.aspectRatio || "1:1";
    imagePrompt = `Commercial photography for ${adv.brandName} ${adv.productName}. 
    Scene: ${adv.mainPrompt}. 
    Style: ${adv.artisticStyle}. 
    Location: ${adv.location}. 
    Quality: 4k, studio lighting, professional. 
    Constraints: Avoid ${adv.negativeConstraints}.`;
    
    // Add reference images if they exist
    if (adv.brandLogo) {
      imageParts.push({ inlineData: { mimeType: 'image/png', data: adv.brandLogo.split(',')[1] } });
    }
    adv.productReferenceImages.forEach(img => {
      imageParts.push({ inlineData: { mimeType: 'image/png', data: img.split(',')[1] } });
    });
    adv.humanModelImages.forEach(img => {
      imageParts.push({ inlineData: { mimeType: 'image/png', data: img.split(',')[1] } });
    });
  } else {
    imagePrompt = `A high-end commercial product photograph for "${input}". Studio lighting, cinematic composition, 4k.`;
  }

  imageParts.push({ text: imagePrompt });

  const imageResponse = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image',
    contents: { parts: imageParts },
    config: {
      imageConfig: {
        aspectRatio: aspectRatio
      }
    }
  });

  let imageUrl = 'https://picsum.photos/800/800'; // Fallback
  // Iterate through parts to find the image part specifically, as per best practices
  if (imageResponse.candidates && imageResponse.candidates[0].content.parts) {
    for (const part of imageResponse.candidates[0].content.parts) {
      if (part.inlineData) {
        imageUrl = `data:image/png;base64,${part.inlineData.data}`;
        break;
      }
    }
  }

  return {
    headline: adCopy.headline || '',
    body: adCopy.body || '',
    hashtags: adCopy.hashtags || [],
    imageUrl: imageUrl
  };
};
