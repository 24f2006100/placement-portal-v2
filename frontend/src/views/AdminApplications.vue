<template>
  <div>
    <Navbar />

    <main class="applications-page">

      <!-- PAGE HEADER -->
      <div class="page-header">

        <div>
          <p class="page-label">
            ADMIN MANAGEMENT
          </p>

          <h1>Manage Applications</h1>

          <p class="page-description">
            View and manage student applications across all placement drives.
          </p>
        </div>


        <div class="application-count">
          <span>Total Applications</span>
          <strong>{{ applications.length }}</strong>
        </div>

      </div>


      <!-- LOADING STATE -->
      <div
        v-if="loading"
        class="state-card"
      >
        Loading applications...
      </div>


      <!-- EMPTY STATE -->
      <div
        v-else-if="applications.length === 0"
        class="state-card"
      >

        <div class="empty-icon">
          A
        </div>

        <h3>No applications found</h3>

        <p>
          There are currently no student applications on the portal.
        </p>

      </div>


      <!-- APPLICATIONS TABLE -->
      <div
        v-else
        class="table-card"
      >

        <div class="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Application</th>
                <th>Student</th>
                <th>Company</th>
                <th>Drive</th>
                <th>Status</th>
                <th>Applied At</th>
                <th>Interview</th>
                <th>Feedback</th>
                <th>Action</th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="application in applications"
                :key="application.id"
              >

                <!-- APPLICATION ID -->
                <td>
                  <span class="application-id">
                    #{{ application.id }}
                  </span>
                </td>


                <!-- STUDENT -->
                <td>

                  <div class="student-info">

                    <div class="student-avatar">
                      {{
                        application.student
                          ? application.student
                              .charAt(0)
                              .toUpperCase()
                          : "S"
                      }}
                    </div>

                    <strong>
                      {{ application.student }}
                    </strong>

                  </div>

                </td>


                <!-- COMPANY -->
                <td>
                  <strong class="company-name">
                    {{ application.company }}
                  </strong>
                </td>


                <!-- DRIVE -->
                <td>
                  {{ application.drive }}
                </td>


                <!-- STATUS -->
                <td>

                  <span
                    class="status-badge"
                    :class="statusClass(application.status)"
                  >
                    {{ application.status }}
                  </span>

                </td>


                <!-- APPLIED AT -->
                <td>
                  {{ application.applied_at || "-" }}
                </td>


                <!-- INTERVIEW -->
                <td>

                  <span
                    v-if="application.interview_date"
                    class="interview-scheduled"
                  >
                    {{ application.interview_date }}
                  </span>

                  <span
                    v-else
                    class="muted-text"
                  >
                    Not Scheduled
                  </span>

                </td>


                <!-- FEEDBACK -->
                <td>

                  <span
                    v-if="application.feedback"
                    class="feedback-text"
                  >
                    {{ application.feedback }}
                  </span>

                  <span
                    v-else
                    class="muted-text"
                  >
                    No Feedback
                  </span>

                </td>


                <!-- ACTION -->
                <td>

                  <button
                    class="delete-button"
                    @click="
                      deleteApplication(application.id)
                    "
                  >
                    Delete
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </main>
  </div>
</template>


<script setup>

import { onMounted, ref } from "vue"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const applications = ref([])
const loading = ref(true)


// =====================================
// LOAD APPLICATIONS
// =====================================

async function loadApplications() {

  try {

    const response = await api.get(
      "/admin/applications"
    )

    applications.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to load applications"
    )

  } finally {

    loading.value = false

  }

}


// =====================================
// STATUS CLASS
// =====================================

function statusClass(status) {

  if (!status) return ""


  return status
    .toLowerCase()
    .replace(/\s+/g, "-")

}


// =====================================
// DELETE APPLICATION
// =====================================

async function deleteApplication(id) {

  const confirmed = confirm(
    "Are you sure you want to delete this application?"
  )


  if (!confirmed) return


  try {

    const response = await api.delete(
      `/admin/application/${id}`
    )


    alert(response.data.message)


    await loadApplications()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to delete application"
    )

  }

}


onMounted(loadApplications)

</script>


<style scoped>

.applications-page {
  max-width: 1450px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}


/* =========================
   PAGE HEADER
========================= */

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  margin-bottom: 30px;
}

.page-label {
  margin: 0 0 8px;
  color: #5c6ac4;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.5px;
}

.page-header h1 {
  margin: 0;
  color: #212529;
  font-size: 32px;
}

.page-description {
  margin: 8px 0 0;
  color: #6c757d;
}


/* =========================
   APPLICATION COUNT
========================= */

.application-count {
  min-width: 160px;
  padding: 16px 22px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.application-count span {
  display: block;
  margin-bottom: 4px;
  color: #6c757d;
  font-size: 13px;
}

.application-count strong {
  color: #212529;
  font-size: 26px;
}


/* =========================
   TABLE
========================= */

.table-card {
  overflow: hidden;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8f9fa;
}

th {
  padding: 15px 16px;
  color: #060708;
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #dee2e6;
}

td {
  padding: 16px;
  color: #495057;
  font-size: 14px;
  vertical-align: middle;
  border-bottom: 1px solid #eeeeee;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #fafbfc;
}


/* =========================
   APPLICATION
========================= */

.application-id {
  color: #5c6ac4;
  font-weight: 700;
}


/* =========================
   STUDENT
========================= */

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 150px;
}

.student-avatar {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 50%;
  font-weight: 700;
}

.company-name {
  color: #343a40;
}


/* =========================
   STATUS
========================= */

.status-badge {
  display: inline-block;
  padding: 6px 11px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}


/* DEFAULT / APPLIED */

.status-badge.applied {
  color: #055160;
  background: #cff4fc;
}


/* SHORTLISTED */

.status-badge.shortlisted {
  color: #664d03;
  background: #fff3cd;
}


/* INTERVIEW */

.status-badge.interview,
.status-badge.interview-scheduled {
  color: #5c3d99;
  background: #eee5ff;
}


/* SELECTED / PLACED */

.status-badge.selected,
.status-badge.placed {
  color: #146c43;
  background: #d1e7dd;
}


/* REJECTED */

.status-badge.rejected {
  color: #b02a37;
  background: #f8d7da;
}


/* WITHDRAWN */

.status-badge.withdrawn {
  color: #495057;
  background: #e9ecef;
}


/* =========================
   INTERVIEW / FEEDBACK
========================= */

.interview-scheduled {
  color: #5c3d99;
  font-weight: 600;
  white-space: nowrap;
}

.feedback-text {
  display: inline-block;
  max-width: 220px;
  color: #495057;
  line-height: 1.4;
}

.muted-text {
  color: #adb5bd;
  font-size: 13px;
  white-space: nowrap;
}


/* =========================
   DELETE
========================= */

.delete-button {
  padding: 7px 12px;
  color: #b02a37;
  background: white;
  border: 1px solid #dc3545;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.delete-button:hover {
  color: white;
  background: #dc3545;
}


/* =========================
   LOADING / EMPTY
========================= */

.state-card {
  padding: 50px 20px;
  text-align: center;
  color: #6c757d;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.empty-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 10px;
  font-size: 20px;
  font-weight: 700;
}

.state-card h3 {
  margin: 0 0 7px;
  color: #343a40;
}

.state-card p {
  margin: 0;
}


/* =========================
   RESPONSIVE
========================= */

@media (max-width: 700px) {

  .applications-page {
    padding: 25px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .application-count {
    width: 100%;
  }

}

</style>