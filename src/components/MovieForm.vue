<template>
  <div>
    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>

    <!-- Error Messages -->
    <div v-if="errors.length > 0" class="alert alert-danger" role="alert">
      <ul class="mb-0">
        <li v-for="error in errors" :key="error.field">
          {{ error.message }}
        </li>
      </ul>
    </div>

    <!-- Upload Form -->
    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input 
          type="text" 
          name="title" 
          id="title" 
          class="form-control"
        />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea 
          name="description" 
          id="description" 
          class="form-control" 
          rows="4"
        ></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input 
          type="file" 
          name="poster" 
          id="poster" 
          class="form-control"
          accept="image/*"
        />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

let csrf_token = ref('');
let successMessage = ref('');
let errors = ref([]);

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.log('Error fetching CSRF token:', error);
    });
}

function saveMovie() {
  // Clear previous messages
  successMessage.value = '';
  errors.value = [];

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
      if (data.message) {
        // Success
        successMessage.value = data.message;
        movieForm.reset(); // Clear form
      } else if (data.errors) {
        // Validation errors
        errors.value = data.errors;
      }
    })
    .catch(function (error) {
      console.log('Error:', error);
      errors.value = [{ field: 'general', message: 'An error occurred. Please try again.' }];
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>