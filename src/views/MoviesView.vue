<template>
  <div class="container mt-5">
    <div class="row mb-4">
      <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center">
          <h1>Movies</h1>
          <router-link to="/movies/create" class="btn btn-primary">
            <i class="bi bi-plus-circle me-2"></i>Add New Movie
          </router-link>
        </div>
        <hr>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3">Loading movies...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="movies.length === 0" class="alert alert-info text-center py-5">
      <h4>No movies added yet</h4>
      <p class="mb-3">Get started by adding your first movie!</p>
      <router-link to="/movies/create" class="btn btn-primary">
        Add Your First Movie
      </router-link>
    </div>

    <!-- Movies Grid -->
    <div v-else class="row">
      <div 
        v-for="movie in movies" 
        :key="movie.id" 
        class="col-md-4 col-sm-6 mb-4"
      >
        <div class="card h-100 movie-card">
          <img 
            :src="movie.poster" 
            class="card-img-top" 
            :alt="movie.title"
            loading="lazy"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text flex-grow-1">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Reactive properties
let movies = ref([]);
let isLoading = ref(true);

/**
 * Fetch all movies from API
 */
function fetchMovies() {
  isLoading.value = true;
  
  fetch('/api/v1/movies')
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
      isLoading.value = false;
    })
    .catch((error) => {
      console.error('Error fetching movies:', error);
      isLoading.value = false;
    });
}

// Fetch movies when component mounts
onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.movie-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-img-top {
  height: 400px;
  object-fit: cover;
  background-color: #f8f9fa;
}

.card-title {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.card-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}
</style>