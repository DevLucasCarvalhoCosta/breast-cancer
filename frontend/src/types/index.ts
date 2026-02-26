export interface SampleWithFeatures {
  id: number;
  original_id: number;
  diagnosis: string;
  diagnosis_encoded: number;
  created_at: string;
  features: Record<string, number>;
}

export interface DatasetStats {
  total_samples: number;
  benign_count: number;
  malignant_count: number;
  benign_percentage: number;
  malignant_percentage: number;
  total_features: number;
}

export interface FeatureDefinitionResponse {
  id: number;
  name: string;
  description: string;
  base_feature: string;
  aggregation: string;
  unit: string;
  min_value: number;
  max_value: number;
  clinical_relevance: string;
}
