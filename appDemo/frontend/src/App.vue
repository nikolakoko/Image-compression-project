<template>
  <div id="app">
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="text-center text-white">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Compressing image...</p>
      </div>
    </div>

    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <!-- Header -->
          <div class="text-center mb-5">
            <h1 class="display-4 fw-bold text-primary">
              <i class="fas fa-compress-alt me-3"></i>Image Compressor
            </h1>
            <p class="lead text-muted">Upload and compress your images with various algorithms</p>
          </div>

          <div class="card shadow-lg border-0">
            <div class="card-body p-4">
              <form @submit.prevent="compressImage">
                <!-- File Upload Section -->
                <div class="mb-4">
                  <h5 class="card-title mb-3">
                    <i class="fas fa-upload me-2"></i>Upload Image
                  </h5>
                  <div
                      class="upload-area"
                      :class="{ dragover: isDragOver }"
                      @click="$refs.fileInput.click()"
                      @dragover.prevent="isDragOver = true"
                      @dragleave.prevent="isDragOver = false"
                      @drop.prevent="handleDrop"
                  >
                    <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
                    <h6>Drag and drop your image here</h6>
                    <p class="text-muted mb-3">or click to browse files</p>
                    <input
                        ref="fileInput"
                        type="file"
                        accept="image/*"
                        class="d-none"
                        @change="handleFileSelect"
                    >
                    <button type="button" class="btn btn-outline-primary">
                      Choose File
                    </button>
                  </div>

                  <div v-if="selectedFile" class="mt-3">
                    <div class="alert alert-info">
                      <i class="fas fa-file-image me-2"></i>
                      {{ selectedFile.name }}
                      <span class="badge bg-primary ms-2">{{ formatFileSize(selectedFile.size) }}</span>
                    </div>
                  </div>
                </div>

                <!-- Image Preview -->
                <div v-if="previewUrl" class="mb-4">
                  <h5 class="card-title mb-3">
                    <i class="fas fa-eye me-2"></i>Preview
                  </h5>
                  <div class="preview-container">
                    <img :src="previewUrl" class="preview-image" alt="Preview">
                  </div>
                </div>

                <!-- Compression Method Selection -->
                <div class="mb-4">
                  <h5 class="card-title mb-3">
                    <i class="fas fa-cogs me-2"></i>Compression Method
                  </h5>
                  <div class="row g-3">
                    <div class="col-md-6 col-lg-3" v-for="method in compressionMethods" :key="method.id">
                      <div
                          class="card method-card h-100"
                          :class="{ selected: selectedMethod === method.id }"
                          @click="selectMethod(method.id)"
                      >
                        <div class="card-body text-center">
                          <i :class="`fas ${method.icon} fa-2x ${method.color} mb-2`"></i>
                          <h6 class="card-title">{{ method.name }}</h6>
                          <p class="card-text small text-muted">{{ method.description }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Compression Parameters -->
                <div class="mb-4">
                  <h5 class="card-title mb-3">
                    <i class="fas fa-sliders-h me-2"></i>Parameters
                  </h5>
                  <div class="row">
                    <div class="col-md-6">
                      <div v-if="showQualitySlider">
                        <label for="quality" class="form-label">Quality (1-100)</label>
                        <input
                            type="range"
                            class="form-range"
                            id="quality"
                            min="1"
                            max="100"
                            v-model="quality"
                        >
                        <div class="d-flex justify-content-between small text-muted">
                          <span>Low</span>
                          <span>{{ quality }}</span>
                          <span>High</span>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div v-if="showKSlider">
                        <label for="k" class="form-label">K Value (Colors)</label>
                        <input
                            type="range"
                            class="form-range"
                            id="k"
                            min="2"
                            max="32"
                            v-model="k"
                        >
                        <div class="d-flex justify-content-between small text-muted">
                          <span>2</span>
                          <span>{{ k }}</span>
                          <span>32</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="text-center">
                  <button
                      type="submit"
                      class="btn btn-primary btn-lg px-5"
                      :disabled="!canCompress"
                  >
                    <i class="fas fa-compress-alt me-2"></i>Compress Image
                  </button>
                </div>
              </form>

              <!-- Results Section -->
              <div v-if="downloadUrl" class="mt-5">
                <hr>
                <h5 class="card-title text-success">
                  <i class="fas fa-check-circle me-2"></i>Compression Complete
                </h5>
                <div class="alert alert-success">
                  <p class="mb-0">Your image has been compressed successfully!</p>
                  <p class="mt-2 mb-0">
                    <a
                        :href="downloadUrl"
                        :download="downloadFilename"
                        class="btn btn-success"
                    >
                      <i class="fas fa-download me-2"></i>Download Compressed Image
                    </a>
                  </p>
                </div>
              </div>

              <!-- Error Section -->
              <div v-if="errorMessage" class="mt-3">
                <div class="alert alert-danger">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ errorMessage }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // Configuration
      apiBaseUrl: 'http://localhost:5000',

      // File handling
      selectedFile: null,
      previewUrl: null,
      isDragOver: false,

      // Compression settings
      selectedMethod: '',
      quality: 20,
      k: 8,

      // UI state
      isLoading: false,
      errorMessage: '',
      downloadUrl: '',
      downloadFilename: '',

      // Compression methods
      compressionMethods: [
        {
          id: 'jpeg',
          name: 'JPEG',
          description: 'Lossy compression for photos',
          icon: 'fa-file-image',
          color: 'text-warning'
        },
        {
          id: 'png',
          name: 'PNG',
          description: 'Lossless compression',
          icon: 'fa-file-image',
          color: 'text-info'
        },
        {
          id: 'kmeans',
          name: 'K-Means',
          description: 'Color quantization',
          icon: 'fa-palette',
          color: 'text-success'
        },
        {
          id: 'rle',
          name: 'RLE',
          description: 'Run-length encoding',
          icon: 'fa-compress',
          color: 'text-danger'
        }
      ]
    }
  },
  computed: {
    canCompress() {
      return this.selectedFile && this.selectedMethod;
    },
    showQualitySlider() {
      return this.selectedMethod === 'jpeg' || this.selectedMethod === 'png';
    },
    showKSlider() {
      return this.selectedMethod === 'kmeans';
    }
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.processFile(file);
      }
    },

    handleDrop(event) {
      this.isDragOver = false;
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.processFile(files[0]);
      }
    },

    processFile(file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        this.showError('Please select a valid image file.');
        return;
      }

      this.selectedFile = file;
      this.errorMessage = '';
      this.downloadUrl = '';

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    selectMethod(methodId) {
      this.selectedMethod = methodId;
      this.errorMessage = '';
      this.downloadUrl = '';
    },

    async compressImage() {
      if (!this.selectedFile || !this.selectedMethod) {
        this.showError('Please select a file and compression method.');
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';
      this.downloadUrl = '';

      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('method', this.selectedMethod);

      if (this.selectedMethod === 'jpeg' || this.selectedMethod === 'png') {
        formData.append('quality', this.quality);
      } else if (this.selectedMethod === 'kmeans') {
        formData.append('k', this.k);
      }

      try {
        const response = await fetch(`${this.apiBaseUrl}/api/compress`, {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const blob = await response.blob();
          this.downloadUrl = URL.createObjectURL(blob);

          // Get filename from Content-Disposition header or use default
          const contentDisposition = response.headers.get('Content-Disposition');
          this.downloadFilename = 'compressed_image';
          if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
            if (matches != null && matches[1]) {
              this.downloadFilename = matches[1].replace(/['"]/g, '');
            }
          }
        } else {
          const error = await response.json();
          this.showError(error.error || 'Compression failed. Please try again.');
        }
      } catch (error) {
        console.error('Compression error:', error);
        this.showError('Network error. Please check if the server is running.');
      } finally {
        this.isLoading = false;
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    showError(message) {
      this.errorMessage = message;
      this.downloadUrl = '';
    }
  }
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #007bff;
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover {
  border-color: #0056b3;
  background-color: #e3f2fd;
}

.upload-area.dragover {
  border-color: #28a745;
  background-color: #d4edda;
}

.preview-container {
  max-height: 300px;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.preview-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.method-card {
  transition: transform 0.2s ease;
  cursor: pointer;
}

.method-card:hover {
  transform: translateY(-2px);
}

.method-card.selected {
  border-color: #007bff;
  background-color: #e3f2fd;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
</style>