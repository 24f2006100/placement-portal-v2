<template>
  <nav class="navbar">

    <div class="navbar-brand">
      Placement Portal
    </div>

    <div class="navbar-links">

      <template v-if="role === 'admin'">
        <router-link to="/admin/dashboard">
          Dashboard
        </router-link>

        <router-link to="/admin/companies">
          Companies
        </router-link>

        <router-link to="/admin/students">
          Students
        </router-link>

        <router-link to="/admin/drives">
          Drives
        </router-link>

        <router-link to="/admin/applications">
          Applications
        </router-link>
      </template>


      <template v-if="role === 'company'">
        <router-link to="/company/dashboard">
          Dashboard
        </router-link>
      </template>


      <template v-if="role === 'student'">
        <router-link to="/student/dashboard">
          Dashboard
        </router-link>
      </template>


      <button
        class="logout-button"
        @click="logout"
      >
        Logout
      </button>

    </div>

  </nav>
</template>


<script setup>

import { useRouter } from "vue-router"

const router = useRouter()

const role = localStorage.getItem("role")


function logout() {

  localStorage.removeItem("token")
  localStorage.removeItem("role")

  router.push("/")

}

</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background: #212529;
}

.navbar-brand {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.navbar-links a {
  color: white;
  text-decoration: none;
}

.navbar-links a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}

.logout-button {
  padding: 7px 15px;
  cursor: pointer;
}
</style>