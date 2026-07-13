<template>
  <div>
    <Navbar />

    <main class="admin-dashboard">

      <!-- PAGE HEADER -->
      <section class="dashboard-header">
        <div>
          <p class="eyebrow">ADMIN PORTAL</p>
          <h1>Admin Dashboard</h1>
          <p class="subtitle">
            Manage placement activities, monitor portal statistics,
            and generate reports.
          </p>
        </div>
      </section>


      <!-- DASHBOARD STATISTICS -->
      <section class="dashboard-section">

        <div class="section-heading">
          <div>
            <h2>Portal Overview</h2>
            <p>Current statistics from the placement portal.</p>
          </div>
        </div>

        <p v-if="loading" class="loading-message">
          Loading dashboard statistics...
        </p>

        <div v-else class="stats-grid">

          <div class="stat-card">
            <span class="stat-label">Total Students</span>
            <strong class="stat-value">
              {{ dashboard.total_students ?? 0 }}
            </strong>
          </div>

          <div class="stat-card">
            <span class="stat-label">Total Companies</span>
            <strong class="stat-value">
              {{ dashboard.total_companies ?? 0 }}
            </strong>
          </div>

          <div class="stat-card">
            <span class="stat-label">Pending Companies</span>
            <strong class="stat-value">
              {{ dashboard.pending_companies ?? 0 }}
            </strong>
          </div>

          <div class="stat-card">
            <span class="stat-label">Approved Companies</span>
            <strong class="stat-value">
              {{ dashboard.approved_companies ?? 0 }}
            </strong>
          </div>

          <div class="stat-card">
            <span class="stat-label">Placement Drives</span>
            <strong class="stat-value">
              {{ dashboard.total_drives ?? 0 }}
            </strong>
          </div>

          <div class="stat-card">
            <span class="stat-label">Applications</span>
            <strong class="stat-value">
              {{ dashboard.total_applications ?? 0 }}
            </strong>
          </div>

        </div>

      </section>


      <!-- QUICK MANAGEMENT -->
      <section class="dashboard-section">

        <div class="section-heading">
          <div>
            <h2>Quick Management</h2>
            <p>Access the main administration sections.</p>
          </div>
        </div>

        <div class="management-grid">

          <button
            class="management-card"
            @click="router.push('/admin/companies')"
          >
            <span class="management-title">
              Companies
            </span>

            <span class="management-description">
              Review, approve, reject and manage registered companies.
            </span>

            <span class="management-link">
              Manage Companies →
            </span>
          </button>


          <button
            class="management-card"
            @click="router.push('/admin/students')"
          >
            <span class="management-title">
              Students
            </span>

            <span class="management-description">
              View, search and manage registered students.
            </span>

            <span class="management-link">
              Manage Students →
            </span>
          </button>


          <button
            class="management-card"
            @click="router.push('/admin/drives')"
          >
            <span class="management-title">
              Placement Drives
            </span>

            <span class="management-description">
              Review, approve, reject and remove placement drives.
            </span>

            <span class="management-link">
              Manage Drives →
            </span>
          </button>


          <button
            class="management-card"
            @click="router.push('/admin/applications')"
          >
            <span class="management-title">
              Applications
            </span>

            <span class="management-description">
              View and manage student placement applications.
            </span>

            <span class="management-link">
              Manage Applications →
            </span>
          </button>

        </div>

      </section>


      <!-- EXPORTS -->
      <section class="dashboard-section">

        <div class="section-heading">
          <div>
            <h2>Data Exports</h2>
            <p>
              Generate CSV files using Celery background jobs.
            </p>
          </div>
        </div>

        <div class="action-grid">

          <button
            class="action-button"
            @click="generateExport('students')"
          >
            Generate Students CSV
          </button>

          <button
            class="action-button"
            @click="generateExport('companies')"
          >
            Generate Companies CSV
          </button>

          <button
            class="action-button"
            @click="generateExport('applications')"
          >
            Generate Applications CSV
          </button>

          <button
            class="action-button"
            @click="generateExport('placements')"
          >
            Generate Placements CSV
          </button>

        </div>

      </section>

      <!-- DOWNLOADS -->
      <section class="dashboard-section">

        <div class="section-heading">
          <div>
            <h2>Download Generated Files</h2>
            <p>
              Generate a file first, then download the latest version.
            </p>
          </div>
        </div>

        <div class="download-grid">

          <button
            class="download-button"
            @click="downloadFile('students.csv')"
          >
            Download Students
          </button>

          <button
            class="download-button"
            @click="downloadFile('companies.csv')"
          >
            Download Companies
          </button>

          <button
            class="download-button"
            @click="downloadFile('applications.csv')"
          >
            Download Applications
          </button>

          <button
            class="download-button"
            @click="downloadFile('placements.csv')"
          >
            Download Placements
          </button>

        </div>

      </section>

    </main>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"

const router = useRouter()

const dashboard = ref({})
const loading = ref(true)

async function loadDashboard() {
  try {
    const response = await api.get("/admin/dashboard")
    dashboard.value = response.data

  } catch (error) {
    alert(
      error.response?.data?.message ||
      "Failed to load dashboard statistics"
    )

  } finally {
    loading.value = false
  }
}

async function generateExport(type) {
  try {
    const response = await api.get(
      `/admin/export/${type}`
    )

    alert(response.data.message)

  } catch (error) {
    alert(
      error.response?.data?.message ||
      "Failed to start CSV export"
    )
  }
}

async function downloadFile(filename) {
  try {
    const response = await api.get(
      `/admin/download/${filename}`,
      {
        responseType: "blob"
      }
    )

    const url = window.URL.createObjectURL(
      new Blob([response.data])
    )

    const link = document.createElement("a")

    link.href = url
    link.setAttribute("download", filename)

    document.body.appendChild(link)

    link.click()
    link.remove()

    window.URL.revokeObjectURL(url)

  } catch (error) {
    alert(
      "Unable to download file. Generate the file first."
    )
  }
}


onMounted(loadDashboard)
</script>


<style scoped>
.admin-dashboard {
  max-width: 1250px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}


/* ================================
   HEADER
================================ */

.dashboard-header {
  margin-bottom: 35px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #6c757d;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 34px;
  color: #212529;
}

.subtitle {
  margin-top: 10px;
  color: #6c757d;
  font-size: 16px;
}


/* ================================
   SECTIONS
================================ */

.dashboard-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.section-heading h2 {
  margin: 0;
  font-size: 21px;
  color: #212529;
}

.section-heading p {
  margin: 6px 0 0;
  color: #6c757d;
  font-size: 14px;
}


/* ================================
   STATISTICS
================================ */

.stats-grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.stat-card {
  padding: 22px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f8f9fa;
}

.stat-label {
  display: block;
  margin-bottom: 12px;
  color: #6c757d;
  font-size: 14px;
}

.stat-value {
  display: block;
  font-size: 30px;
  color: #212529;
}

.loading-message {
  color: #6c757d;
}


/* ================================
   MANAGEMENT CARDS
================================ */

.management-grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fit, minmax(230px, 1fr));
  gap: 16px;
}

.management-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-height: 170px;
  padding: 22px;
  text-align: left;
  background: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.management-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px
    rgba(0, 0, 0, 0.08);
}

.management-title {
  margin-bottom: 10px;
  font-size: 19px;
  font-weight: 700;
  color: #212529;
}

.management-description {
  flex: 1;
  color: #6c757d;
  line-height: 1.5;
}

.management-link {
  margin-top: 18px;
  font-weight: 600;
}


/* ================================
   ACTIONS
================================ */

.action-grid,
.download-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.action-button,
.download-button,
.primary-button {
  padding: 11px 18px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

.action-button {
  background: #f8f9fa;
  border: 1px solid #ced4da;
}

.download-button {
  background: white;
  border: 1px solid #6c757d;
}

.primary-button {
  background: #212529;
  color: white;
  border: 1px solid #212529;
}

.action-button:hover,
.download-button:hover {
  background: #e9ecef;
}

.primary-button:hover {
  opacity: 0.9;
}


/* ================================
   RESPONSIVE
================================ */

@media (max-width: 700px) {
  .admin-dashboard {
    padding: 25px 15px 40px;
  }

  .dashboard-header h1 {
    font-size: 28px;
  }

  .dashboard-section {
    padding: 18px;
  }

  .action-button,
  .download-button,
  .primary-button {
    width: 100%;
  }
}
</style>