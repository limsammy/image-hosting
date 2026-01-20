import apiClient from './client';

export interface UploadUrlRequest {
  filename: string;
  content_type: string;
}

export interface UploadUrlResponse {
  upload_url: string;
  image_key: string;
}

export interface ConfirmUploadRequest {
  image_key: string;
  filename: string;
  content_type: string;
  size: number;
}

export interface Image {
  id: string;
  filename: string;
  size: number;
  content_type: string;
  image_key: string;
  image_url: string;
  created_at: string;
  user_id: string;
}

export interface ListImagesResponse {
  images: Image[];
  total: number;
  page: number;
  page_size: number;
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
  listImages: async (page = 1, pageSize = 20): Promise<ListImagesResponse> => {
    const response = await apiClient.get<ListImagesResponse>('/images/', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  /**
   * Delete an image
   */
  deleteImage: async (imageId: string): Promise<void> => {
    await apiClient.delete(`/images/${imageId}`);
  },
};
