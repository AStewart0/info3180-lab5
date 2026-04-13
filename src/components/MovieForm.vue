<template>
  <div class="movie-form-container">
    <!-- Success Message (Bonus) -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      <strong>Success!</strong> {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''" aria-label="Close"></button>
    </div>

    <!-- Error Messages (Bonus) -->
    <div v-if="errors.length > 0" class="alert alert-danger alert-dismissible fade show" role="alert">
      <strong>Please fix the following errors:</strong>
      <ul class="mb-0 mt-2">
        <li v-for="error in errors" :key="error.field">
          {{ error.message }}
        </li>
      </ul>
      <button type="button" class="btn-close" @click="errors = []" aria-label="Close"></button>
    </div>

    <!-- Upload Form -->
    <div class="card">
      <div class="card-body">
        <h2 class="card-title mb-4">Upload Form</h2>
        
        <form id="movieForm" @submit.prevent="saveMovie">
          <!-- Movie Title Field -->
          <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input 
              type="text" 
              name="title" 
              id="title" 
              class="form-control"
              placeholder="Enter movie title"
            />
          </div>

          <!-- Description Field -->
          <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea 
              name="description" 
              id="description" 
              class="form-control" 
              rows="4"
              placeholder="Enter movie description or summary"
            ></textarea>
          </div>

          <!-- Photo Upload Field -->
          <div class="form-group mb-3">
            <label for="poster" class="form-label">Photo Upload</label>
            <input 
              type="file" 
              name="poster" 
              id="poster" 
              class="form-control"
              accept="image/*"
            />
            <small class="form-text text-muted">
              Accepted formats: JPG, JPEG, PNG, GIF
            </small>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
            <span v-if="isSubmitting">
              <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Uploading...
            </span>
            <span v-else>Submit</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Reactive properties
let csrf_token = ref('');
let successMessage = ref('');
let errors = ref([]);
let isSubmitting = ref(false);

/**
 * Fetch CSRF token from Flask API
 */
function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
      console.log('CSRF token fetched successfully');
    })
    .catch((error) => {
      console.error('Error fetching CSRF token:', error);
    });
}

/**
 * Save movie to database via API
 */
function saveMovie() {
  // Clear previous messages
  successMessage.value = '';
  errors.value = [];
  isSubmitting.value = true;

  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      isSubmitting.value = false;
      
      if (data.message) {
        // Success response
        successMessage.value = data.message;
        movieForm.reset(); // Clear the form
        
        // Scroll to top to show success message
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (data.errors) {
        // Validation errors
        errors.value = data.errors;
        
        // Scroll to top to show errors
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    })
    .catch(function (error) {
      isSubmitting.value = false;
      console.error('Error:', error);
      errors.value = [{ 
        field: 'general', 
        message: 'An error occurred while uploading. Please try again.' 
      }];
    });
}

// Fetch CSRF token when component mounts
onMounted(() => {
  getCsrfToken();
});
</script>

<style scoped>
.movie-form-container {
  max-width: 600px;
  margin: 0 auto;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.alert {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 500;
}
</style>