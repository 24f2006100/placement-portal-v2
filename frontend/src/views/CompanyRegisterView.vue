<template>
  <div class="container">
    <div class="auth-card">

      <h1>Placement Portal</h1>
      <h2>Company Registration</h2>

      <form @submit.prevent="registerCompany">

        <div class="form-group">
          <label>Representative Full Name</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="Enter representative name"
            required
          />
        </div>

        <div class="form-group">
          <label>Login Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="Enter login email"
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
          <label>Company Name</label>
          <input
            v-model="form.company_name"
            type="text"
            placeholder="Enter company name"
            required
          />
        </div>

        <div class="form-group">
          <label>Website</label>
          <input
            v-model="form.website"
            type="text"
            placeholder="Example: https://company.com"
          />
        </div>

        <div class="form-group">
          <label>HR Name</label>
          <input
            v-model="form.hr_name"
            type="text"
            placeholder="Enter HR name"
          />
        </div>

        <div class="form-group">
          <label>HR Email</label>
          <input
            v-model="form.hr_email"
            type="email"
            placeholder="Enter HR email"
          />
        </div>

        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? "Registering..." : "Register Company" }}
        </button>

      </form>

      <p v-if="message">{{ message }}</p>

      <div class="links">
        <router-link to="/">
          Already registered? Login
        </router-link>

        <router-link to="/student/register">
          Register as Student
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
  company_name: "",
  website: "",
  hr_name: "",
  hr_email: ""
})

async function registerCompany() {
  try {
    loading.value = true
    message.value = ""

    const response = await api.post("/register/company", form)

    alert(
      response.data.message +
      "\nYour account is pending admin approval."
    )

    router.push("/")

  } catch (error) {
    message.value =
      error.response?.data?.message ||
      "Company registration failed"
  } finally {
    loading.value = false
  }
}
</script>