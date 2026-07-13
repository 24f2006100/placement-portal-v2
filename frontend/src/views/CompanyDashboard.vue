<template>
  <div>
    <Navbar />

    <main class="company-page">

      <!-- LOADING -->
      <div
        v-if="loading"
        class="state-card"
      >
        Loading company dashboard...
      </div>


      <!-- PENDING / REJECTED COMPANY -->
      <div
        v-else-if="status !== 'Approved'"
        class="approval-card"
      >
        <div class="status-icon">
          {{ status === "Rejected" ? "!" : "..." }}
        </div>

        <p class="page-label">
          COMPANY PORTAL
        </p>

        <h1>Account Status: {{ status }}</h1>

        <p>
          {{ message }}
        </p>
      </div>


      <!-- APPROVED COMPANY -->
      <div v-else>

        <!-- =========================
             PAGE HEADER
        ========================== -->
        <div class="page-header">

          <div>
            <p class="page-label">
              COMPANY PORTAL
            </p>

            <h1>{{ companyName }} Dashboard</h1>

            <p class="page-description">
              Create placement drives and manage your recruitment activities.
            </p>
          </div>

        </div>


        <!-- =========================
             DASHBOARD STATISTICS
        ========================== -->
        <div class="stats-grid">

          <div class="stat-card">
            <span>Total Drives</span>

            <strong>
              {{ dashboard.total_drives }}
            </strong>
          </div>


          <div class="stat-card approved-stat">
            <span>Approved Drives</span>

            <strong>
              {{ dashboard.approved_drives }}
            </strong>
          </div>


          <div class="stat-card pending-stat">
            <span>Pending Drives</span>

            <strong>
              {{ dashboard.pending_drives }}
            </strong>
          </div>

        </div>


        <!-- =========================
             CREATE PLACEMENT DRIVE
        ========================== -->
        <section class="content-card">

          <div class="section-header">
            <div>
              <h2>Create Placement Drive</h2>

              <p>
                Add a new recruitment opportunity for eligible students.
              </p>
            </div>
          </div>


          <form
            class="drive-form"
            @submit.prevent="createDrive"
          >

            <div class="form-grid">

              <!-- TITLE -->
              <div class="form-group full-width">
                <label>Job Title</label>

                <input
                  v-model="drive.title"
                  type="text"
                  placeholder="Example: Software Engineer"
                  required
                />
              </div>


              <!-- DESCRIPTION -->
              <div class="form-group full-width">
                <label>Job Description</label>

                <textarea
                  v-model="drive.description"
                  placeholder="Enter the job description..."
                  required
                ></textarea>
              </div>


              <!-- SALARY -->
              <div class="form-group">
                <label>Salary Package</label>

                <input
                  v-model="drive.salary_package"
                  type="number"
                  step="0.01"
                  placeholder="Example: 12.5"
                  required
                />
              </div>


              <!-- LOCATION -->
              <div class="form-group">
                <label>Location</label>

                <input
                  v-model="drive.location"
                  type="text"
                  placeholder="Example: Bangalore"
                  required
                />
              </div>


              <!-- BRANCH -->
              <div class="form-group">
                <label>Branch Required</label>

                <input
                  v-model="drive.branch_required"
                  type="text"
                  placeholder="Example: CSE"
                  required
                />
              </div>


              <!-- CGPA -->
              <div class="form-group">
                <label>Minimum CGPA</label>

                <input
                  v-model="drive.cgpa_required"
                  type="number"
                  step="0.01"
                  placeholder="Example: 7.5"
                  required
                />
              </div>


              <!-- DEADLINE -->
              <div class="form-group full-width">
                <label>Application Deadline</label>

                <input
                  v-model="drive.deadline"
                  type="date"
                  required
                />
              </div>

            </div>


            <p
              v-if="formMessage"
              class="form-message"
            >
              {{ formMessage }}
            </p>


            <button
              type="submit"
              class="primary-button"
            >
              Create Placement Drive
            </button>

          </form>

        </section>


        <!-- =========================
             MY PLACEMENT DRIVES
        ========================== -->
        <section class="content-card">

          <div class="section-header">

            <div>
              <h2>My Placement Drives</h2>

              <p>
                View and manage all placement drives created by your company.
              </p>
            </div>


            <div class="drive-count">
              {{ drives.length }}
              {{ drives.length === 1 ? "Drive" : "Drives" }}
            </div>

          </div>


          <!-- NO DRIVES -->
          <div
            v-if="drives.length === 0"
            class="empty-state"
          >
            <h3>No placement drives yet</h3>

            <p>
              Create your first placement drive using the form above.
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
                  <th>Drive</th>
                  <th>Location</th>
                  <th>Package</th>
                  <th>Branch</th>
                  <th>CGPA</th>
                  <th>Deadline</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>


              <tbody>

                <tr
                  v-for="item in drives"
                  :key="item.id"
                >

                  <!-- DRIVE -->
                  <td>
                    <div class="drive-info">

                      <div class="drive-avatar">
                        {{
                          item.title
                            ? item.title
                                .charAt(0)
                                .toUpperCase()
                            : "D"
                        }}
                      </div>

                      <div>
                        <strong>
                          {{ item.title }}
                        </strong>

                        <span>
                          Drive #{{ item.id }}
                        </span>
                      </div>

                    </div>
                  </td>


                  <!-- LOCATION -->
                  <td>
                    {{ item.location }}
                  </td>


                  <!-- PACKAGE -->
                  <td>
                    <strong>
                      {{ item.salary_package }}
                    </strong>
                  </td>


                  <!-- BRANCH -->
                  <td>
                    <span class="branch-badge">
                      {{ item.branch_required }}
                    </span>
                  </td>


                  <!-- CGPA -->
                  <td>
                    {{ item.cgpa_required }}
                  </td>


                  <!-- DEADLINE -->
                  <td>
                    {{ item.deadline }}
                  </td>


                  <!-- STATUS -->
                  <td>
                    <span
                      class="status-badge"
                      :class="
                        item.status
                          ?.toLowerCase()
                      "
                    >
                      {{ item.status }}
                    </span>
                  </td>


                  <!-- ACTIONS -->
                  <td>

                    <div class="action-buttons">

                      <button
                        class="view-button"
                        @click="
                          viewApplicants(item.id)
                        "
                      >
                        Applicants
                      </button>


                      <button
                        class="edit-button"
                        @click="startEdit(item)"
                      >
                        Edit
                      </button>


                      <button
                        v-if="item.status !== 'Closed'"
                        class="close-button"
                        @click="closeDrive(item.id)"
                      >
                        Close
                      </button>


                      <button
                        v-if="item.status === 'Closed'"
                        class="open-button"
                        @click="openDrive(item.id)"
                      >
                        Reopen
                      </button>


                      <button
                        class="delete-button"
                        @click="deleteDrive(item.id)"
                      >
                        Delete
                      </button>

                    </div>

                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </section>


        <!-- =========================
             EDIT PLACEMENT DRIVE
        ========================== -->
        <section
          v-if="editingDrive"
          class="content-card edit-card"
        >

          <div class="section-header">

            <div>
              <p class="edit-label">
                EDITING DRIVE #{{ editingDrive }}
              </p>

              <h2>Edit Placement Drive</h2>

              <p>
                Update the placement drive information below.
              </p>
            </div>

          </div>


          <form
            class="drive-form"
            @submit.prevent="updateDrive"
          >

            <div class="form-grid">

              <div class="form-group full-width">
                <label>Job Title</label>

                <input
                  v-model="editForm.title"
                  type="text"
                  required
                />
              </div>


              <div class="form-group">
                <label>Salary Package</label>

                <input
                  v-model="editForm.salary_package"
                  type="number"
                  step="0.01"
                  required
                />
              </div>


              <div class="form-group">
                <label>Location</label>

                <input
                  v-model="editForm.location"
                  type="text"
                  required
                />
              </div>


              <div class="form-group">
                <label>Branch Required</label>

                <input
                  v-model="editForm.branch_required"
                  type="text"
                  required
                />
              </div>


              <div class="form-group">
                <label>Minimum CGPA</label>

                <input
                  v-model="editForm.cgpa_required"
                  type="number"
                  step="0.01"
                  required
                />
              </div>


              <div class="form-group full-width">
                <label>Application Deadline</label>

                <input
                  v-model="editForm.deadline"
                  type="date"
                  required
                />
              </div>

            </div>


            <div class="edit-actions">

              <button
                type="submit"
                class="primary-button"
              >
                Save Changes
              </button>


              <button
                type="button"
                class="cancel-button"
                @click="cancelEdit"
              >
                Cancel
              </button>

            </div>

          </form>

        </section>

      </div>

    </main>
  </div>
</template>


<script setup>

import { onMounted, reactive, ref } from "vue"
import { useRouter } from "vue-router"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const router = useRouter()

const loading = ref(true)
const status = ref("")
const message = ref("")
const companyName = ref("")
const formMessage = ref("")
const drives = ref([])
const editingDrive = ref(null)


const dashboard = reactive({
  total_drives: 0,
  approved_drives: 0,
  pending_drives: 0
})


const drive = reactive({
  title: "",
  description: "",
  salary_package: "",
  location: "",
  branch_required: "",
  cgpa_required: "",
  deadline: ""
})


const editForm = reactive({
  title: "",
  salary_package: "",
  location: "",
  branch_required: "",
  cgpa_required: "",
  deadline: ""
})


// =====================================
// LOAD DASHBOARD
// =====================================

async function loadDashboard() {

  try {

    const response = await api.get(
      "/company/dashboard"
    )


    status.value = response.data.status

    message.value =
      response.data.message || ""


    if (status.value === "Approved") {

      companyName.value =
        response.data.company_name

      dashboard.total_drives =
        response.data.total_drives

      dashboard.approved_drives =
        response.data.approved_drives

      dashboard.pending_drives =
        response.data.pending_drives


      await loadDrives()

    }

  } catch (error) {

    message.value =
      error.response?.data?.message ||
      "Unable to load company dashboard"

  } finally {

    loading.value = false

  }

}


// =====================================
// LOAD DRIVES
// =====================================

async function loadDrives() {

  try {

    const response = await api.get(
      "/company/drives"
    )

    drives.value = response.data

  } catch (error) {

    console.error(error)

  }

}


// =====================================
// CREATE DRIVE
// =====================================

async function createDrive() {

  try {

    formMessage.value = ""


    const response = await api.post(
      "/company/create-drive",
      {
        title: drive.title,

        description:
          drive.description,

        salary_package:
          Number(drive.salary_package),

        location:
          drive.location,

        branch_required:
          drive.branch_required,

        cgpa_required:
          Number(drive.cgpa_required),

        deadline:
          drive.deadline
      }
    )


    alert(response.data.message)


    drive.title = ""
    drive.description = ""
    drive.salary_package = ""
    drive.location = ""
    drive.branch_required = ""
    drive.cgpa_required = ""
    drive.deadline = ""


    await loadDashboard()

  } catch (error) {

    formMessage.value =
      error.response?.data?.message ||
      "Failed to create placement drive"

  }

}


// =====================================
// CLOSE DRIVE
// =====================================

async function closeDrive(id) {

  try {

    const response = await api.put(
      `/company/drive/${id}/close`
    )

    alert(response.data.message)

    await loadDashboard()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to close drive"
    )

  }

}


// =====================================
// REOPEN DRIVE
// =====================================

async function openDrive(id) {

  try {

    const response = await api.put(
      `/company/drive/${id}/open`
    )

    alert(response.data.message)

    await loadDashboard()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to reopen drive"
    )

  }

}


// =====================================
// DELETE DRIVE
// =====================================

async function deleteDrive(id) {

  const confirmed = confirm(
    "Are you sure you want to delete this drive?"
  )


  if (!confirmed) return


  try {

    const response = await api.delete(
      `/company/drive/${id}`
    )

    alert(response.data.message)

    await loadDashboard()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to delete drive"
    )

  }

}


// =====================================
// START EDIT
// =====================================

function startEdit(item) {

  editingDrive.value = item.id


  editForm.title =
    item.title

  editForm.salary_package =
    item.salary_package

  editForm.location =
    item.location

  editForm.branch_required =
    item.branch_required

  editForm.cgpa_required =
    item.cgpa_required

  editForm.deadline =
    item.deadline


  // Move to edit form
  setTimeout(() => {

    document
      .querySelector(".edit-card")
      ?.scrollIntoView({
        behavior: "smooth"
      })

  }, 100)

}


// =====================================
// CANCEL EDIT
// =====================================

function cancelEdit() {

  editingDrive.value = null

}


// =====================================
// UPDATE DRIVE
// =====================================

async function updateDrive() {

  try {

    const response = await api.put(
      `/company/drive/${editingDrive.value}`,
      {
        title:
          editForm.title,

        salary_package:
          Number(editForm.salary_package),

        location:
          editForm.location,

        branch_required:
          editForm.branch_required,

        cgpa_required:
          Number(editForm.cgpa_required),

        deadline:
          editForm.deadline
      }
    )


    alert(response.data.message)


    editingDrive.value = null


    await loadDashboard()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to update placement drive"
    )

  }

}


// =====================================
// VIEW APPLICANTS
// =====================================

function viewApplicants(driveId) {

  router.push(
    `/company/applicants/${driveId}`
  )

}


onMounted(loadDashboard)

</script>


<style scoped>

.company-page {
  max-width: 1350px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}


/* PAGE HEADER */

.page-header {
  margin-bottom: 30px;
}

.page-label,
.edit-label {
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


/* STATISTICS */

.stats-grid {
  display: grid;
  grid-template-columns:
    repeat(3, minmax(0, 1fr));
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
  font-size: 30px;
}

.approved-stat {
  background: #f4faf6;
  border-color: #dcecdf;
}

.approved-stat strong {
  color: #2d8a49;
}

.pending-stat {
  background: #fffaf1;
  border-color: #f2e7d2;
}

.pending-stat strong {
  color: #d88400;
}


/* CONTENT CARDS */

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

.drive-count {
  padding: 8px 13px;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
}


/* FORM */

.drive-form {
  max-width: 900px;
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

.form-group input,
.form-group textarea {
  padding: 11px 13px;
  color: #343a40;
  background: white;
  border: 1px solid #ced4da;
  border-radius: 7px;
  font-family: inherit;
  font-size: 14px;
  outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #6c7ae0;
}

.form-group textarea {
  min-height: 110px;
  resize: vertical;
}

.form-message {
  margin: 18px 0 0;
  color: #b02a37;
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


/* TABLE */

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
  padding: 14px;
  color: #060708;
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #dee2e6;
}

td {
  padding: 15px 14px;
  color: #495057;
  font-size: 14px;
  white-space: nowrap;
  border-bottom: 1px solid #eeeeee;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #fafbfc;
}


/* DRIVE */

.drive-info {
  display: flex;
  align-items: center;
  gap: 11px;
}

.drive-avatar {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 9px;
  font-weight: 700;
}

.drive-info strong {
  display: block;
  color: #212529;
}

.drive-info span {
  display: block;
  margin-top: 3px;
  color: #868e96;
  font-size: 11px;
}


/* BADGES */

.branch-badge,
.status-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.branch-badge {
  color: #495057;
  background: #f1f3f5;
}

.status-badge.pending {
  color: #9a6700;
  background: #fff3cd;
}

.status-badge.approved,
.status-badge.open {
  color: #146c43;
  background: #d1e7dd;
}

.status-badge.rejected {
  color: #b02a37;
  background: #f8d7da;
}

.status-badge.closed {
  color: #495057;
  background: #e9ecef;
}


/* ACTIONS */

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.action-buttons button {
  padding: 6px 9px;
  background: white;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}

.view-button {
  color: #4f5fc7;
  border: 1px solid #6c7ae0;
}

.edit-button {
  color: #495057;
  border: 1px solid #adb5bd;
}

.close-button {
  color: #9a6700;
  border: 1px solid #d6a100;
}

.open-button {
  color: #146c43;
  border: 1px solid #198754;
}

.delete-button {
  color: #b02a37;
  border: 1px solid #dc3545;
}


/* EDIT */

.edit-card {
  border-left: 4px solid #5c6ac4;
}

.edit-actions {
  display: flex;
  gap: 10px;
}

.cancel-button {
  margin-top: 20px;
  padding: 11px 20px;
  color: #495057;
  background: white;
  border: 1px solid #adb5bd;
  border-radius: 7px;
  font-weight: 600;
  cursor: pointer;
}


/* STATES */

.state-card,
.approval-card {
  padding: 50px 25px;
  text-align: center;
  color: #6c757d;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.approval-card {
  max-width: 650px;
  margin: 50px auto;
}

.approval-card h1 {
  margin: 12px 0;
  color: #212529;
}

.status-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 18px;
  color: #9a6700;
  background: #fff3cd;
  border-radius: 50%;
  font-weight: 700;
}

.empty-state {
  padding: 35px;
  text-align: center;
  color: #6c757d;
  background: #fafbfc;
  border-radius: 8px;
}

.empty-state h3 {
  margin: 0 0 7px;
  color: #343a40;
}

.empty-state p {
  margin: 0;
}


/* RESPONSIVE */

@media (max-width: 750px) {

  .company-page {
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

}

</style>