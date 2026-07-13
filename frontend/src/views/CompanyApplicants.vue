<template>
  <div>
    <Navbar />

    <main class="applicants-page">

      <!-- PAGE HEADER -->
      <div class="page-header">

        <div>
          <p class="page-label">
            COMPANY PORTAL
          </p>

          <h1>Drive Applicants</h1>

          <p class="page-description">
            Review applicants and manage each student's recruitment progress.
          </p>
        </div>


        <div class="header-actions">

          <div class="applicant-count">
            <span>Applicants</span>
            <strong>{{ applicants.length }}</strong>
          </div>

          <button
            class="back-button"
            @click="goBack"
          >
            ← Back to Dashboard
          </button>

        </div>

      </div>


      <!-- LOADING STATE -->
      <div
        v-if="loading"
        class="state-card"
      >
        Loading applicants...
      </div>


      <!-- EMPTY STATE -->
      <div
        v-else-if="applicants.length === 0"
        class="state-card"
      >

        <div class="empty-icon">
          A
        </div>

        <h3>No applicants yet</h3>

        <p>
          No students have applied for this placement drive yet.
        </p>

      </div>


      <!-- APPLICANTS TABLE -->
      <div
        v-else
        class="table-card"
      >

        <div class="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Student</th>
                <th>Email</th>
                <th>Branch</th>
                <th>CGPA</th>
                <th>Phone</th>
                <th>Resume</th>
                <th>Applied On</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="applicant in applicants"
                :key="applicant.application_id"
              >

                <!-- STUDENT -->
                <td>

                  <div class="student-info">

                    <div class="student-avatar">
                      {{
                        applicant.student_name
                          ? applicant.student_name
                              .charAt(0)
                              .toUpperCase()
                          : "S"
                      }}
                    </div>

                    <div>
                      <strong>
                        {{ applicant.student_name }}
                      </strong>

                      <span>
                        Application
                        #{{ applicant.application_id }}
                      </span>
                    </div>

                  </div>

                </td>


                <!-- EMAIL -->
                <td>
                  {{ applicant.email }}
                </td>


                <!-- BRANCH -->
                <td>
                  <span class="branch-badge">
                    {{ applicant.branch || "Not Provided" }}
                  </span>
                </td>


                <!-- CGPA -->
                <td>
                  <strong class="cgpa-value">
                    {{
                      applicant.cgpa !== null &&
                      applicant.cgpa !== undefined
                        ? applicant.cgpa
                        : "-"
                    }}
                  </strong>
                </td>


                <!-- PHONE -->
                <td>
                  {{ applicant.phone || "Not Provided" }}
                </td>

                <!-- RESUME -->
                 <td>

                <button
                    v-if="applicant.has_resume"
                    class="resume-button"
                    @click="
                    viewResume(
                        applicant.application_id
                    )">
                    View Resume
                </button>

                <span
                    v-else
                    class="no-resume"
                >
                    Not Uploaded
                </span>
                </td>


                <!-- APPLIED AT -->
                <td>
                  {{ applicant.applied_at || "-" }}
                </td>


                <!-- STATUS -->
                <td>

                  <span
                    class="status-badge"
                    :class="statusClass(applicant.status)"
                  >
                    {{ applicant.status }}
                  </span>

                </td>


                <!-- ACTIONS -->
                <td>

                  <div class="action-buttons">

                    <button
                      class="shortlist-button"
                      @click="
                        shortlist(
                          applicant.application_id
                        )
                      "
                    >
                      Shortlist
                    </button>


                    <button
                      class="reject-button"
                      @click="
                        reject(
                          applicant.application_id
                        )
                      "
                    >
                      Reject
                    </button>


                    <button
                      class="interview-button"
                      @click="
                        scheduleInterview(
                          applicant.application_id
                        )
                      "
                    >
                      Interview
                    </button>


                    <button
                      class="offer-button"
                      @click="
                        releaseOffer(
                          applicant.application_id
                        )
                      "
                    >
                      Offer
                    </button>


                    <button
                      v-if="
                        applicant.status !== 'Placed'
                      "
                      class="place-button"
                      @click="
                        placeStudent(
                          applicant.application_id
                        )
                      "
                    >
                      Place
                    </button>


                    <span
                      v-else
                      class="placed-label"
                    >
                      Placed
                    </span>


                    <button
                      class="feedback-button"
                      @click="
                        addFeedback(
                          applicant.application_id
                        )
                      "
                    >
                      Feedback
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
import { useRoute, useRouter } from "vue-router"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const route = useRoute()
const router = useRouter()

const driveId = route.params.driveId

const applicants = ref([])
const loading = ref(true)


// =====================================
// LOAD APPLICANTS
// =====================================

async function loadApplicants() {

  try {

    const response = await api.get(
      `/company/applicants/${driveId}`
    )

    applicants.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to load applicants"
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
// VIEW RESUME
// =====================================
async function viewResume(applicationId) {

  try {

    const response = await api.get(
      `/company/application/${applicationId}/resume`,
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
      error.response?.data?.message ||
      "Failed to open resume"
    )

  }

}


// =====================================
// SHORTLIST
// =====================================

async function shortlist(id) {

  try {

    const response = await api.put(
      `/company/application/${id}/shortlist`
    )

    alert(response.data.message)

    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to shortlist applicant"
    )

  }

}


// =====================================
// REJECT
// =====================================

async function reject(id) {

  try {

    const response = await api.put(
      `/company/application/${id}/reject`
    )

    alert(response.data.message)

    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to reject applicant"
    )

  }

}


// =====================================
// SCHEDULE INTERVIEW
// =====================================

async function scheduleInterview(id) {

  const interviewDate = prompt(
    "Enter interview date and time in this format:\nYYYY-MM-DD HH:MM"
  )


  if (!interviewDate) return


  try {

    const response = await api.put(
      `/company/application/${id}/schedule`,
      {
        interview_date: interviewDate
      }
    )


    alert(response.data.message)


    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to schedule interview"
    )

  }

}


// =====================================
// RELEASE OFFER
// =====================================

async function releaseOffer(id) {

  try {

    const response = await api.put(
      `/company/application/${id}/offer`
    )


    alert(response.data.message)


    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to release offer"
    )

  }

}


// =====================================
// PLACE STUDENT
// =====================================

async function placeStudent(id) {

  const confirmed = confirm(
    "Mark this student as placed?"
  )


  if (!confirmed) return


  try {

    const response = await api.put(
      `/company/application/${id}/place`
    )


    alert(response.data.message)


    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to mark student as placed"
    )

  }

}


// =====================================
// ADD FEEDBACK
// =====================================

async function addFeedback(id) {

  const feedback = prompt(
    "Enter feedback for this applicant:"
  )


  if (!feedback) return


  try {

    const response = await api.put(
      `/company/application/${id}/feedback`,
      {
        feedback: feedback
      }
    )


    alert(response.data.message)


    // Refresh in case feedback is later
    // displayed in the API response.
    await loadApplicants()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to add feedback"
    )

  }

}


// =====================================
// BACK TO DASHBOARD
// =====================================

function goBack() {

  router.push(
    "/company/dashboard"
  )

}


onMounted(loadApplicants)

</script>


<style scoped>

.applicants-page {
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
   HEADER ACTIONS
========================= */

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.applicant-count {
  min-width: 110px;
  padding: 12px 18px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.applicant-count span {
  display: block;
  color: #6c757d;
  font-size: 12px;
}

.applicant-count strong {
  display: block;
  margin-top: 3px;
  color: #212529;
  font-size: 23px;
}

.back-button {
  padding: 10px 15px;
  color: #495057;
  background: white;
  border: 1px solid #ced4da;
  border-radius: 7px;
  font-weight: 600;
  cursor: pointer;
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
   STUDENT
========================= */

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.student-avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #4f5fc7;
  background: #eef0ff;
  border-radius: 50%;
  font-weight: 700;
}

.student-info strong {
  display: block;
  color: #212529;
}

.student-info span {
  display: block;
  margin-top: 3px;
  color: #868e96;
  font-size: 11px;
}

/* =========================
   RESUME
========================= */
.resume-button {
  padding: 7px 11px;
  color: #4f5fc7;
  background: white;
  border: 1px solid #4f5fc7;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.resume-button:hover {
  color: white;
  background: #4f5fc7;
}

.no-resume {
  color: #adb5bd;
  font-size: 12px;
}

/* =========================
   BRANCH / CGPA
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

.cgpa-value {
  color: #212529;
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
   ACTIONS
========================= */

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  min-width: 360px;
}

.action-buttons button {
  padding: 6px 9px;
  background: white;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}

.shortlist-button {
  color: #9a6700;
  border: 1px solid #d6a100;
}

.reject-button {
  color: #b02a37;
  border: 1px solid #dc3545;
}

.interview-button {
  color: #5c3d99;
  border: 1px solid #8065d7;
}

.offer-button {
  color: #146c43;
  border: 1px solid #198754;
}

.place-button {
  color: white;
  background: #198754 !important;
  border: 1px solid #198754;
}

.feedback-button {
  color: #495057;
  border: 1px solid #adb5bd;
}

.placed-label {
  display: inline-flex;
  align-items: center;
  padding: 6px 9px;
  color: #146c43;
  background: #d1e7dd;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 700;
}


/* =========================
   STATES
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
  border-radius: 50%;
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

@media (max-width: 750px) {

  .applicants-page {
    padding: 25px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    align-items: stretch;
    flex-direction: column;
  }

  .applicant-count {
    width: auto;
  }

}

</style>