export interface BackendAdRequest {
  main_prompt: string;
  info_type: "basic" | "advanced";

  brand_name?: string | null;
  product_name?: string | null;
  brand_logo?: string | null;

  product_reference_images?: string[];
  human_model_images?: string[];

  artistic_style?: string | null;
  aspect_ratio?: "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9";

  location?: string | null;
  language?: string | null;

  negative_constraints?: string | null;
  target_audience?: string | null;
  call_to_action?: string | null;
  additional_information?: string | null;
}




export interface AdContent {
  headline: string;
  body: string;
  hashtags: string[];
  imageUrl: string; 
}

export interface AdvancedInput {
  mainPrompt: string;
  brandName: string;
  productName: string;
  brandLogo?: string;
  productReferenceImages: string[];
  humanModelImages: string[];
  artisticStyle: string;
  aspectRatio: "1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9";
  location: string;
  language: string;
  negativeConstraints: string;
  targetAudience: string;
  callToAction: string;
  additionalInfo: string;
}

export enum AppStatus {
  IDLE = 'IDLE',
  LOADING = 'LOADING',
  SUCCESS = 'SUCCESS',
  ERROR = 'ERROR'
}
