<template>
  <div>
    <Navbar />

    <main class="drives-page">

      <!-- PAGE HEADER -->
      <div class="page-header">

        <div>
          <p class="page-label">
            ADMIN MANAGEMENT
          </p>

          <h1>Placement Drives</h1>

          <p class="page-description">
            Review, approve and manage placement drives created by companies.
          </p>
        </div>


        <div class="drive-count">
          <span>Drives Shown</span>
          <strong>{{ drives.length }}</strong>
        </div>

      </div>


      <!-- LOADING STATE -->
      <div
        v-if="loading"
        class="state-card"
      >
        Loading placement drives...
      </div>


      <!-- EMPTY STATE -->
      <div
        v-else-if="drives.length === 0"
        class="state-card"
      >
        <div class="empty-icon">
          D
        </div>

        <h3>No placement drives found</h3>

        <p>
          There are currently no placement drives available.
        </p>
      </div>


      <!-- DRIVES TABLE -->
      <div
        v-else
        class="table-card"
      >

        <div class="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Drive</th>
                <th>Company</th>
                <th>Location</th>
                <th>Package</th>
                <th>Branch</th>
                <th>Minimum CGPA</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="drive in drives"
                :key="drive.id"
              >

                <!-- DRIVE -->
                <td>

                  <div class="drive-info">

                    <div class="drive-avatar">
                      {{
                        drive.title
                          ? drive.title
                              .charAt(0)
                              .toUpperCase()
                          : "D"
                      }}
                    </div>

                    <div>
                      <strong>
                        {{ drive.title }}
                      </strong>

                      <span class="drive-id">
                        Drive #{{ drive.id }}
                      </span>
                    </div>

                  </div>

                </td>


                <!-- COMPANY -->
                <td>
                  <strong class="company-name">
                    {{ drive.company }}
                  </strong>
                </td>


                <!-- LOCATION -->
                <td>
                  {{ drive.location || "Not Provided" }}
                </td>


                <!-- PACKAGE -->
                <td>
                  <span class="package-value">
                    {{
                      drive.salary_package !== null &&
                      drive.salary_package !== undefined
                        ? drive.salary_package
                        : "-"
                    }}
                  </span>
                </td>


                <!-- BRANCH -->
                <td>
                  <span class="branch-badge">
                    {{ drive.branch_required || "Any" }}
                  </span>
                </td>


                <!-- CGPA -->
                <td>
                  <span class="cgpa-value">
                    {{
                      drive.cgpa_required !== null &&
                      drive.cgpa_required !== undefined
                        ? drive.cgpa_required
                        : "-"
                    }}
                  </span>
                </td>


                <!-- DEADLINE -->
                <td>
                  {{ drive.deadline || "-" }}
                </td>


                <!-- STATUS -->
                <td>

                  <span
                    class="status-badge"
                    :class="
                      drive.status
                        ?.toLowerCase()
                    "
                  >
                    {{ drive.status }}
                  </span>

                </td>


                <!-- ACTIONS -->
                <td>

                  <div class="action-buttons">

                    <button
                      v-if="drive.status === 'Pending'"
                      class="approve-button"
                      @click="approveDrive(drive.id)"
                    >
                      Approve
                    </button>


                    <button
                      v-if="drive.status === 'Pending'"
                      class="reject-button"
                      @click="rejectDrive(drive.id)"
                    >
                      Reject
                    </button>


                    <span
                      v-if="drive.status !== 'Pending'"
                      class="processed-text"
                    >
                      Processed
                    </span>


                    <button
                      class="delete-button"
                      @click="deleteDrive(drive.id)"
                    >
                      Delete
                    </button>

                  </div>

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


const drives = ref([])
const loading = ref(true)


// =====================================
// LOAD DRIVES
// =====================================

async function loadDrives() {

  try {

    const response = await api.get(
      "/admin/drives"
    )

    drives.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to load placement drives"
    )

  } finally {

    loading.value = false

  }

}


// =====================================
// APPROVE DRIVE
// =====================================

async function approveDrive(id) {

  const confirmed = confirm(
    "Are you sure you want to approve this placement drive?"
  )

  if (!confirmed) return


  try {

    const response = await api.put(
      `/admin/drive/${id}/approve`
    )

    alert(response.data.message)

    await loadDrives()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to approve placement drive"
    )

  }

}


// =====================================
// REJECT DRIVE
// =====================================

async function rejectDrive(id) {

  const confirmed = confirm(
    "Are you sure you want to reject this placement drive?"
  )

  if (!confirmed) return


  try {

    const response = await api.put(
      `/admin/drive/${id}/reject`
    )

    alert(response.data.message)

    await loadDrives()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to reject placement drive"
    )

  }

}


// =====================================
// DELETE DRIVE
// =====================================

async function deleteDrive(id) {

  const confirmed = confirm(
    "Are you sure you want to delete this placement drive?"
  )

  if (!confirmed) return


  try {

    const response = await api.delete(
      `/admin/drive/${id}`
    )

    alert(response.data.message)

    await loadDrives()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to delete placement drive"
    )

  }

}


onMounted(loadDrives)

</script>


<style scoped>

.drives-page {
  max-width: 1400px;
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
   DRIVE COUNT
========================= */

.drive-count {
  min-width: 150px;
  padding: 16px 22px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.drive-count span {
  display: block;
  margin-bottom: 4px;
  color: #6c757d;
  font-size: 13px;
}

.drive-count strong {
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
  white-space: nowrap;
  border-bottom: 1px solid #eeeeee;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #fafbfc;
}


/* =========================
   DRIVE INFORMATION
========================= */

.drive-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.drive-avatar {
  width: 40px;
  height: 40px;
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

.drive-id {
  display: block;
  margin-top: 3px;
  color: #868e96;
  font-size: 11px;
}

.company-name {
  color: #343a40;
}


/* =========================
   PACKAGE / CGPA
========================= */

.package-value,
.cgpa-value {
  font-weight: 700;
  color: #212529;
}


/* =========================
   BRANCH
========================= */

.branch-badge {
  display: inline-block;
  padding: 5px 10px;
  color: #495057;
  background: #f1f3f5;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
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
}

.status-badge.pending {
  color: #9a6700;
  background: #fff3cd;
}

.status-badge.approved {
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


/* =========================
   ACTIONS
========================= */

.action-buttons {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
}

.action-buttons button {
  padding: 7px 11px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.approve-button {
  color: #146c43;
  background: #d1e7dd;
  border: 1px solid #a3cfbb;
}

.reject-button {
  color: #b02a37;
  background: #f8d7da;
  border: 1px solid #f1aeb5;
}

.delete-button {
  color: #b02a37;
  background: white;
  border: 1px solid #dc3545;
}

.delete-button:hover {
  color: white;
  background: #dc3545;
}

.processed-text {
  color: #6c757d;
  font-size: 12px;
}


/* =========================
   LOADING / EMPTY STATE
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

  .drives-page {
    padding: 25px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .drive-count {
    width: 100%;
  }

}

</style>