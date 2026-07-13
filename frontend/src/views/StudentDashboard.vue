<template>
  <div>
    <Navbar />

    <main class="student-page">

      <!-- LOADING -->
      <div
        v-if="loading"
        class="state-card"
      >
        Loading student dashboard...
      </div>


      <div v-else>

        <!-- =========================
             PAGE HEADER
        ========================== -->
        <div class="page-header">

          <div>
            <p class="page-label">
              STUDENT PORTAL
            </p>

            <h1>
              Welcome, {{ dashboard.full_name }}
            </h1>

            <p class="page-description">
              Manage your profile, explore placement opportunities,
              and track your applications.
            </p>
          </div>

        </div>


        <!-- =========================
             DASHBOARD STATISTICS
        ========================== -->
        <div class="stats-grid">

          <div class="stat-card branch-stat">
            <span>Branch</span>

            <strong>
              {{ dashboard.branch || "Not Provided" }}
            </strong>
          </div>


          <div class="stat-card cgpa-stat">
            <span>CGPA</span>

            <strong>
              {{ dashboard.cgpa || "-" }}
            </strong>
          </div>


          <div class="stat-card year-stat">
            <span>Graduation Year</span>

            <strong>
              {{ dashboard.graduation_year || "-" }}
            </strong>
          </div>


          <div class="stat-card application-stat">
            <span>Total Applications</span>

            <strong>
              {{ dashboard.total_applications }}
            </strong>
          </div>

        </div>


        <!-- =========================
             UPDATE PROFILE
        ========================== -->
        <section class="content-card">

          <div class="section-header">

            <div>
              <h2>Update Profile</h2>

              <p>
                Keep your academic and contact information up to date.
              </p>
            </div>

          </div>


          <form
            class="profile-form"
            @submit.prevent="updateProfile"
          >

            <div class="form-grid">

              <!-- BRANCH -->
              <div class="form-group">

                <label>Branch</label>

                <input
                  v-model="profile.branch"
                  type="text"
                  placeholder="Example: CSE"
                />

              </div>


              <!-- CGPA -->
              <div class="form-group">

                <label>CGPA</label>

                <input
                  v-model="profile.cgpa"
                  type="number"
                  step="0.01"
                  min="0"
                  max="10"
                  placeholder="Example: 8.5"
                />

              </div>


              <!-- GRADUATION YEAR -->
              <div class="form-group">

                <label>Graduation Year</label>

                <input
                  v-model="profile.graduation_year"
                  type="number"
                  placeholder="Example: 2027"
                />

              </div>


              <!-- PHONE -->
              <div class="form-group">

                <label>Phone</label>

                <input
                  v-model="profile.phone"
                  type="text"
                  placeholder="Enter phone number"
                />

              </div>


              <!-- RESUME -->
              <div class="form-group full-width">

                <label>Resume</label>

                <div class="resume-actions">

                    <input
                    type="file"
                    accept=".pdf,application/pdf"
                    @change="selectResume"
                    />

                    <button
                    type="button"
                    class="upload-resume-button"
                    :disabled="!resumeFile || uploadingResume"
                    @click="uploadResume"
                    >
                    {{
                        uploadingResume
                        ? "Uploading..."
                        : "Upload Resume"
                    }}
                    </button>

                    <button
                    v-if="dashboard.resume"
                    type="button"
                    class="view-resume-button"
                    @click="viewResume"
                    >
                    View Resume
                    </button>

                </div>

                <span
                    v-if="dashboard.resume"
                    class="resume-status"
                >
                    Resume uploaded: {{ dashboard.resume }}
                </span>

                </div>

            </div>


            <button
              type="submit"
              class="primary-button"
            >
              Update Profile
            </button>

          </form>

        </section>


        <!-- =========================
             AVAILABLE DRIVES
        ========================== -->
        <section class="content-card">

          <div class="section-header">

            <div>
              <h2>Available Placement Drives</h2>

              <p>
                Search and apply for approved placement opportunities.
              </p>
            </div>


            <div class="drive-count">
              {{ drives.length }}
              {{ drives.length === 1 ? "Drive" : "Drives" }}
            </div>

          </div>


          <!-- SEARCH -->
          <div class="search-box">

            <input
              v-model="searchTitle"
              type="text"
              placeholder="Search drives by job title..."
              @keyup.enter="searchDrives"
            />


            <button
              class="search-button"
              @click="searchDrives"
            >
              Search
            </button>


            <button
              class="clear-button"
              @click="clearSearch"
            >
              Clear
            </button>

          </div>


          <!-- NO DRIVES -->
          <div
            v-if="drives.length === 0"
            class="empty-state"
          >

            <h3>No placement drives found</h3>

            <p>
              No approved placement drives are currently available.
            </p>

          </div>


          <!-- DRIVES TABLE -->
          <div
            v-else
            class="table-wrapper"
          >

            <table>

              <thead>
                <tr>
                  <th>Company</th>
                  <th>Position</th>
                  <th>Location</th>
                  <th>Package</th>
                  <th>Branch</th>
                  <th>Minimum CGPA</th>
                  <th>Deadline</th>
                  <th>Action</th>
                </tr>
              </thead>


              <tbody>

                <tr
                  v-for="drive in drives"
                  :key="drive.id"
                >

                  <!-- COMPANY -->
                  <td>

                    <div class="company-info">

                      <div class="company-avatar">
                        {{
                          drive.company
                            ? drive.company
                                .charAt(0)
                                .toUpperCase()
                            : "C"
                        }}
                      </div>

                      <strong>
                        {{ drive.company }}
                      </strong>

                    </div>

                  </td>


                  <!-- POSITION -->
                  <td>
                    <strong class="position-name">
                      {{ drive.title }}
                    </strong>
                  </td>


                  <!-- LOCATION -->
                  <td>
                    {{ drive.location || "Not Provided" }}
                  </td>


                  <!-- PACKAGE -->
                  <td>
                    <strong class="package-value">
                      {{ drive.salary_package }}
                    </strong>
                  </td>


                  <!-- BRANCH -->
                  <td>

                    <span class="branch-badge">
                      {{ drive.branch_required }}
                    </span>

                  </td>


                  <!-- CGPA -->
                  <td>
                    {{ drive.cgpa_required }}
                  </td>


                  <!-- DEADLINE -->
                  <td>
                    {{ drive.deadline }}
                  </td>


                  <!-- ACTION -->
                  <td>

                    <button
                      v-if="!hasApplied(drive)"
                      class="apply-button"
                      @click="applyToDrive(drive.id)"
                    >
                      Apply
                    </button>


                    <button
                      v-else
                      class="applied-button"
                      disabled
                    >
                      Applied
                    </button>

                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </section>


        <!-- =========================
             MY APPLICATIONS
        ========================== -->
        <section class="content-card">

          <div class="section-header">

            <div>
              <h2>My Applications</h2>

              <p>
                Track your application status, interviews and feedback.
              </p>
            </div>


            <div class="application-header-actions">

            <div class="application-count">
                {{ applications.length }}
                {{
                applications.length === 1
                    ? "Application"
                    : "Applications"
                }}
            </div>

            <button
                class="export-button"
                :disabled="exporting"
                @click="exportApplications"
            >
                {{
                exporting
                    ? "Preparing CSV..."
                    : "Export Applications"
                }}
            </button>

            </div>

          </div>


          <!-- NO APPLICATIONS -->
          <div
            v-if="applications.length === 0"
            class="empty-state"
          >

            <h3>No applications yet</h3>

            <p>
              You have not applied to any placement drives yet.
            </p>

          </div>


          <!-- APPLICATIONS TABLE -->
          <div
            v-else
            class="table-wrapper"
          >

            <table>

              <thead>
                <tr>
                  <th>Company</th>
                  <th>Position</th>
                  <th>Status</th>
                  <th>Interview Date</th>
                  <th>Feedback</th>
                  <th>Applied At</th>
                  <th>Action</th>
                </tr>
              </thead>


              <tbody>

                <tr
                  v-for="application in applications"
                  :key="application.application_id"
                >

                  <!-- COMPANY -->
                  <td>
                    <strong>
                      {{ application.company }}
                    </strong>
                  </td>


                  <!-- POSITION -->
                  <td>
                    {{ application.title }}
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


                  <!-- INTERVIEW -->
                  <td>

                    <span
                      v-if="application.interview_date"
                      class="interview-date"
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


                  <!-- APPLIED AT -->
                  <td>
                    {{ application.applied_at }}
                  </td>


                  <!-- ACTION -->
                  <td>

                    <button
                      v-if="application.status === 'Applied'"
                      class="withdraw-button"
                      @click="
                        withdrawApplication(
                          application.application_id
                        )
                      "
                    >
                      Withdraw
                    </button>


                    <span
                      v-else
                      class="no-action"
                    >
                      —
                    </span>

                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </section>

      </div>

    </main>
  </div>
</template>


<script setup>

import { onMounted, reactive, ref } from "vue"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const loading = ref(true)

const drives = ref([])
const applications = ref([])
const searchTitle = ref("")
const exporting = ref(false)
const resumeFile = ref(null)
const uploadingResume = ref(false)

const dashboard = reactive({
  full_name: "",
  branch: "",
  cgpa: "",
  graduation_year: "",
  resume: null,
  total_applications: 0
})


const profile = reactive({
  branch: "",
  cgpa: "",
  graduation_year: "",
  phone: "",
})


// =====================================
// LOAD DASHBOARD
// =====================================

async function loadDashboard() {

  try {

    const response = await api.get(
      "/student/dashboard"
    )


    dashboard.full_name =
      response.data.full_name

    dashboard.branch =
      response.data.branch

    dashboard.cgpa =
      response.data.cgpa

    dashboard.graduation_year =
      response.data.graduation_year

    dashboard.resume =
      response.data.resume

    dashboard.total_applications =
      response.data.total_applications

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to load student dashboard"
    )

  }

}


// =====================================
// LOAD DRIVES
// =====================================

async function loadDrives() {

  try {

    const response = await api.get(
      "/student/drives"
    )

    drives.value = response.data

  } catch (error) {

    console.error(error)

  }

}


// =====================================
// LOAD APPLICATIONS
// =====================================

async function loadApplications() {

  try {

    const response = await api.get(
      "/student/applications"
    )

    applications.value = response.data

  } catch (error) {

    console.error(error)

  }

}


// =====================================
// LOAD COMPLETE PAGE
// =====================================

async function loadPage() {

  try {

    await Promise.all([
      loadDashboard(),
      loadDrives(),
      loadApplications()
    ])

  } finally {

    loading.value = false

  }

}

// =====================================
// Resume
// =====================================
function selectResume(event) {

  resumeFile.value =
    event.target.files[0] || null

}
async function uploadResume() {

  if (!resumeFile.value) {
    return
  }


  const formData = new FormData()

  formData.append(
    "resume",
    resumeFile.value
  )


  try {

    uploadingResume.value = true


    const response = await api.post(
      "/student/resume",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data"
        }
      }
    )


    alert(response.data.message)

    resumeFile.value = null

    await loadDashboard()


  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to upload resume"
    )

  } finally {

    uploadingResume.value = false

  }

}
async function viewResume() {

  try {

    const response = await api.get(
      "/student/resume",
      {
        responseType: "blob"
      }
    )


    const url =
      window.URL.createObjectURL(
        new Blob(
          [response.data],
          {
            type: "application/pdf"
          }
        )
      )


    window.open(
      url,
      "_blank"
    )


    setTimeout(
      () => {
        window.URL.revokeObjectURL(url)
      },
      60000
    )


  } catch (error) {

    alert(
      "Failed to open resume"
    )

  }

}


// =====================================
// APPLY TO DRIVE
// =====================================

async function applyToDrive(driveId) {

  try {

    const response = await api.post(
      `/student/apply/${driveId}`
    )


    alert(response.data.message)


    await loadDashboard()
    await loadApplications()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to apply"
    )

  }

}


// =====================================
// WITHDRAW APPLICATION
// =====================================

async function withdrawApplication(applicationId) {

  const confirmed = confirm(
    "Are you sure you want to withdraw this application?"
  )


  if (!confirmed) return


  try {

    const response = await api.delete(
      `/student/application/${applicationId}`
    )


    alert(response.data.message)


    await loadDashboard()
    await loadApplications()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to withdraw application"
    )

  }

}


// =====================================
// UPDATE PROFILE
// =====================================

async function updateProfile() {

  try {

    const data = {}


    if (profile.branch !== "") {
      data.branch = profile.branch
    }


    if (profile.cgpa !== "") {
      data.cgpa = Number(profile.cgpa)
    }


    if (profile.graduation_year !== "") {

      data.graduation_year =
        Number(profile.graduation_year)

    }


    if (profile.phone !== "") {
      data.phone = profile.phone
    }

    const response = await api.put(
      "/student/profile",
      data
    )
    alert(response.data.message)

    await loadDashboard()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to update profile"
    )

  }

}

// =====================================
// SEARCH DRIVES
// =====================================

async function searchDrives() {

  try {

    if (!searchTitle.value.trim()) {

      await loadDrives()

      return

    }


    const response = await api.get(
      "/student/search/drives",
      {
        params: {
          title: searchTitle.value
        }
      }
    )


    drives.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to search drives"
    )

  }

}


// =====================================
// CLEAR SEARCH
// =====================================

async function clearSearch() {

  searchTitle.value = ""

  await loadDrives()

}


// =====================================
// CHECK IF ALREADY APPLIED
// =====================================

function hasApplied(drive) {

  return applications.value.some(
    application =>
      application.company === drive.company &&
      application.title === drive.title
  )
}

async function exportApplications() {

  if (exporting.value) return

  exporting.value = true

  try {

    // Start Celery export job
    const response = await api.post(
      "/student/export/applications"
    )

    const taskId = response.data.task_id


    // Check task status one request at a time
    async function checkStatus() {

      try {

        const statusResponse = await api.get(
          `/student/export/status/${taskId}`
        )

        const status = statusResponse.data.status


        // Export completed
        if (status === "SUCCESS") {

          const filename =
            statusResponse.data.filename

          exporting.value = false


          alert(
            "Your application history export is ready."
          )


          // Download CSV
          const downloadResponse = await api.get(
            `/student/export/download/${filename}`,
            {
              responseType: "blob"
            }
          )


          const url =
            window.URL.createObjectURL(
              new Blob([
                downloadResponse.data
              ])
            )


          const link =
            document.createElement("a")


          link.href = url

          link.setAttribute(
            "download",
            filename
          )


          document.body.appendChild(link)

          link.click()

          link.remove()

          window.URL.revokeObjectURL(url)

          return
        }


        // Export failed
        if (status === "FAILURE") {

          exporting.value = false

          alert(
            "Failed to generate application export."
          )

          return
        }


        // Still processing:
        // wait 1 second before checking again
        setTimeout(
          checkStatus,
          1000
        )

      } catch (error) {

        exporting.value = false

        alert(
          "Failed to check export status."
        )

      }

    }


    // Start checking
    checkStatus()


  } catch (error) {

    exporting.value = false

    alert(
      error.response?.data?.message ||
      "Failed to start export"
    )

  }

}

// =====================================
// STATUS CSS CLASS
// =====================================

function statusClass(status) {

  if (!status) return ""

  return status
    .toLowerCase()
    .replace(/\s+/g, "-")

}


onMounted(loadPage)

</script>


<style scoped>

.student-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}


/* =========================
   PAGE HEADER
========================= */

.page-header {
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
   STATISTICS
========================= */

.stats-grid {
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 25px;
}

.stat-card {
  padding: 22px;
  background: #f7f8ff;
  border: 1px solid #e2e5f5;
  border-radius: 12px;
}

.stat-card span {
  display: block;
  margin-bottom: 10px;
  color: #6c757d;
  font-size: 14px;
}

.stat-card strong {
  color: #4f5fc7;
  font-size: 25px;
}

.cgpa-stat {
  background: #f4faf6;
  border-color: #dcecdf;
}

.cgpa-stat strong {
  color: #2d8a49;
}

.year-stat {
  background: #fffaf1;
  border-color: #f2e7d2;
}

.year-stat strong {
  color: #d88400;
}

.application-stat {
  background: #f8f5ff;
  border-color: #e8e1f8;
}

.application-stat strong {
  color: #7658cf;
}


/* =========================
   CONTENT CARDS
========================= */

.content-card {
  margin-bottom: 25px;
  padding: 25px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.section-header h2 {
  margin: 0;
  color: #212529;
  font-size: 21px;
}

.section-header p {
  margin: 6px 0 0;
  color: #6c757d;
  font-size: 14px;
}

.drive-count,
.application-count {
  padding: 8px 13px;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
}


/* =========================
   PROFILE FORM
========================= */

.profile-form {
  max-width: 1000px;
}

.form-grid {
  display: grid;
  grid-template-columns:
    repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  margin-bottom: 7px;
  color: #495057;
  font-size: 13px;
  font-weight: 600;
}

.form-group input {
  padding: 11px 13px;
  color: #343a40;
  background: white;
  border: 1px solid #ced4da;
  border-radius: 7px;
  font-family: inherit;
  font-size: 14px;
  outline: none;
}

.form-group input:focus {
  border-color: #6c7ae0;
}

.primary-button {
  margin-top: 20px;
  padding: 11px 20px;
  color: white;
  background: #212529;
  border: 1px solid #212529;
  border-radius: 7px;
  font-weight: 600;
  cursor: pointer;
}


/* =========================
   SEARCH
========================= */

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.search-box input {
  flex: 1;
  max-width: 500px;
  padding: 11px 14px;
  border: 1px solid #ced4da;
  border-radius: 7px;
  font-size: 14px;
  outline: none;
}

.search-box input:focus {
  border-color: #6c7ae0;
}

.search-box button {
  padding: 10px 18px;
  border-radius: 7px;
  font-weight: 600;
  cursor: pointer;
}

.search-button {
  color: white;
  background: #212529;
  border: 1px solid #212529;
}

.clear-button {
  color: #495057;
  background: white;
  border: 1px solid #ced4da;
}


/* =========================
   TABLE
========================= */

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
  padding: 15px 14px;
  color: #060708;
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #dee2e6;
}

td {
  padding: 16px 14px;
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
   COMPANY
========================= */

.company-info {
  display: flex;
  align-items: center;
  gap: 11px;
}

.company-avatar {
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

.position-name,
.package-value {
  color: #212529;
}


/* =========================
   BADGES
========================= */

.branch-badge,
.status-badge {
  display: inline-block;
  padding: 6px 11px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.branch-badge {
  color: #495057;
  background: #f1f3f5;
}

.status-badge.applied {
  color: #055160;
  background: #cff4fc;
}

.status-badge.shortlisted {
  color: #664d03;
  background: #fff3cd;
}

.status-badge.interview,
.status-badge.interview-scheduled {
  color: #5c3d99;
  background: #eee5ff;
}

.status-badge.offer-released,
.status-badge.selected,
.status-badge.placed {
  color: #146c43;
  background: #d1e7dd;
}

.status-badge.rejected {
  color: #b02a37;
  background: #f8d7da;
}


/* =========================
   BUTTONS
========================= */

.apply-button,
.applied-button,
.withdraw-button {
  padding: 7px 13px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.apply-button {
  color: white;
  background: #212529;
  border: 1px solid #212529;
  cursor: pointer;
}

.applied-button {
  color: #146c43;
  background: #d1e7dd;
  border: 1px solid #a3cfbb;
  cursor: default;
}

.withdraw-button {
  color: #b02a37;
  background: white;
  border: 1px solid #dc3545;
  cursor: pointer;
}

.withdraw-button:hover {
  color: white;
  background: #dc3545;
}


/* =========================
   APPLICATION DETAILS
========================= */

.interview-date {
  color: #5c3d99;
  font-weight: 600;
  white-space: nowrap;
}

.feedback-text {
  display: inline-block;
  max-width: 220px;
  line-height: 1.4;
}

.muted-text,
.no-action {
  color: #adb5bd;
  font-size: 13px;
}

/* =========================
   RESUME Actions
   ========================= */

.resume-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.upload-resume-button,
.view-resume-button {
  padding: 9px 14px;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.upload-resume-button {
  color: white;
  background: #212529;
  border: 1px solid #212529;
}

.upload-resume-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.view-resume-button {
  color: #4f5fc7;
  background: white;
  border: 1px solid #4f5fc7;
}

.resume-status {
  margin-top: 9px;
  color: #198754;
  font-size: 13px;
}


/* =========================
   EMPTY / LOADING
========================= */

.state-card,
.empty-state {
  padding: 45px 20px;
  text-align: center;
  color: #6c757d;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.empty-state {
  padding: 35px 20px;
  background: #fafbfc;
}

.empty-state h3 {
  margin: 0 0 7px;
  color: #343a40;
}

.empty-state p {
  margin: 0;
}

.application-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.export-button {
  padding: 8px 14px;
  color: white;
  background: #212529;
  border: 1px solid #212529;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.export-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


/* =========================
   RESPONSIVE
========================= */

@media (max-width: 900px) {

  .stats-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

}


@media (max-width: 650px) {

  .student-page {
    padding: 25px 15px;
  }

  .stats-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: auto;
  }

  .section-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .search-box {
    flex-direction: column;
  }

  .search-box input {
    max-width: none;
  }

}

</style>