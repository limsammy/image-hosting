import apiClient from './client';

export interface UploadUrlRequest {
  filename: string;
  content_type: string;
  size_bytes: number;
}

export interface UploadUrlResponse {
  upload_url: string;
  r2_key: string;
  public_url: string;
}

export interface ConfirmUploadRequest {
  r2_key: string;
  filename: string;
  content_type: string;
  size_bytes: number;
}

export interface Image {
  id: number;
  filename: string;
  public_url: string;
  content_type: string;
  size_bytes: number;
  created_at: string;
}

export interface ListImagesResponse {
  images: Image[];
  total: number;
  page: number;
  per_page: number;
}

export const imagesApi = {
  /**
   * Request a presigned URL for uploading an image to R2
   */
  getUploadUrl: async (data: UploadUrlRequest): Promise<UploadUrlResponse> => {
    const response = await apiClient.post<UploadUrlResponse>('/images/upload-url', data);
    return response.data;
  },

  /**
   * Upload image file to R2 using presigned URL
   */
  uploadToR2: async (uploadUrl: string, file: File): Promise<void> => {
    await fetch(uploadUrl, {
      method: 'PUT',
      body: file,
      headers: {
        'Content-Type': file.type,
      },
    });
  },

  /**
   * Confirm upload and save image metadata to database
   */
  confirmUpload: async (data: ConfirmUploadRequest): Promise<Image> => {
    const response = await apiClient.post<Image>('/images/confirm', data);
    return response.data;
  },

  /**
   * List user's images with pagination
   */
  listImages: async (page = 1, perPage = 20): Promise<ListImagesResponse> => {
    const response = await apiClient.get<ListImagesResponse>('/images/', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  /**
   * Delete an image
   */
  deleteImage: async (imageId: number): Promise<void> => {
    await apiClient.delete(`/images/${imageId}`);
  },
};
