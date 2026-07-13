<template>
  <div class="container">
    <div class="auth-card">

      <h1>Placement Portal</h1>
      <h2>Student Registration</h2>

      <form @submit.prevent="registerStudent">

        <div class="form-group">
          <label>Full Name</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="Enter full name"
            required
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            required
          />
        </div>

        <div class="form-group">
          <label>Branch</label>
          <input
            v-model="form.branch"
            type="text"
            placeholder="Example: CSE"
          />
        </div>

        <div class="form-group">
          <label>CGPA</label>
          <input
            v-model="form.cgpa"
            type="number"
            step="0.01"
            min="0"
            max="10"
            placeholder="Example: 8.5"
          />
        </div>

        <div class="form-group">
          <label>Graduation Year</label>
          <input
            v-model="form.graduation_year"
            type="number"
            placeholder="Example: 2027"
          />
        </div>

        <div class="form-group">
          <label>Phone</label>
          <input
            v-model="form.phone"
            type="text"
            placeholder="Enter phone number"
          />
        </div>

        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>

      </form>

      <p v-if="message">{{ message }}</p>

      <div class="links">
        <router-link to="/">
          Already registered? Login
        </router-link>

        <router-link to="/company/register">
          Register as Company
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const message = ref("")
const loading = ref(false)

const form = reactive({
  full_name: "",
  email: "",
  password: "",
  branch: "",
  cgpa: "",
  graduation_year: "",
  phone: ""
})

async function registerStudent() {
  try {
    loading.value = true
    message.value = ""

    const response = await api.post("/register/student", {
      full_name: form.full_name,
      email: form.email,
      password: form.password,
      branch: form.branch,
      cgpa: form.cgpa === "" ? null : Number(form.cgpa),
      graduation_year:
        form.graduation_year === ""
          ? null
          : Number(form.graduation_year),
      phone: form.phone
    })

    alert(response.data.message)

    router.push("/")

  } catch (error) {
    message.value =
      error.response?.data?.message ||
      "Student registration failed"
  } finally {
    loading.value = false
  }
}
</script>