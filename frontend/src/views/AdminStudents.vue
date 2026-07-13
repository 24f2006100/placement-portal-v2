<template>
  <div>
    <Navbar />

    <main class="students-page">

      <div class="page-header">

        <div>
          <p class="page-label">
            ADMIN MANAGEMENT
          </p>

          <h1>Registered Students</h1>

          <p class="page-description">
            Search, view and manage students registered on the portal.
          </p>
        </div>


        <div class="student-count">
          <span>Students Shown</span>
          <strong>{{ students.length }}</strong>
        </div>

      </div>

      <div class="search-section">

        <input
          v-model="searchName"
          type="text"
          placeholder="Search student by name..."
          @keyup.enter="searchStudents"
        />

        <button
          class="search-button"
          @click="searchStudents"
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

      <div
        v-if="students.length === 0"
        class="empty-state"
      >
        <div class="empty-icon">
          S
        </div>

        <h3>No students found</h3>

        <p>
          No registered students match your current search.
        </p>
      </div>

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
                <th>Graduation Year</th>
                <th>Phone</th>
                <th>Action</th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="student in students"
                :key="student.id"
              >

                <!-- STUDENT NAME -->
                <td>

                  <div class="student-info">

                    <div class="student-avatar">
                      {{
                        student.full_name
                          ? student.full_name
                              .charAt(0)
                              .toUpperCase()
                          : "S"
                      }}
                    </div>

                    <strong>
                      {{ student.full_name }}
                    </strong>

                  </div>

                </td>

                <td>
                  {{ student.email }}
                </td>
                <td>
                  <span class="branch-badge">
                    {{ student.branch || "Not Provided" }}
                  </span>
                </td>
                <td>
                  <span class="cgpa-value">
                    {{
                      student.cgpa !== null &&
                      student.cgpa !== undefined
                        ? student.cgpa
                        : "-"
                    }}
                  </span>
                </td>
                <td>
                  {{ student.graduation_year || "-" }}
                </td>
                <td>
                  {{ student.phone || "Not Provided" }}
                </td>
                <td>
                  <button
                    v-if="student.is_active"
                    @click="deactivateStudent(student.id)"
                    >
                    Deactivate
                    </button>

                    <button
                    v-else
                    disabled
                    >
                    Deactivated
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

import { ref, onMounted } from "vue"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const students = ref([])
const searchName = ref("")

async function loadStudents() {

  try {

    const response = await api.get(
      "/admin/students"
    )

    students.value = response.data

  } catch (error) {

    console.log(error)

  }

}

async function searchStudents() {

  try {

    if (!searchName.value.trim()) {

      await loadStudents()

      return

    }

    const response = await api.get(
      "/admin/search/student",
      {
        params: {
          name: searchName.value
        }
      }
    )

    students.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to search students"
    )

  }

}

async function clearSearch() {

  searchName.value = ""

  await loadStudents()

}

async function deactivateStudent(id) {

  const confirmed = confirm(
    "Are you sure you want to deactivate this student?"
  )


  if (!confirmed) return


  try {

    const response = await api.put(
      `/admin/student/${id}/deactivate`
    )


    alert(response.data.message)


    await loadStudents()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to deactivate student"
    )

  }

}


onMounted(loadStudents)

</script>


<style scoped>

.students-page {
  max-width: 1250px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}

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
   STUDENT COUNT
========================= */

.student-count {
  min-width: 150px;
  padding: 16px 22px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.student-count span {
  display: block;
  margin-bottom: 4px;
  color: #6c757d;
  font-size: 13px;
}

.student-count strong {
  color: #212529;
  font-size: 26px;
}


/* =========================
   SEARCH
========================= */

.search-section {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
}

.search-section input {
  flex: 1;
  max-width: 500px;
  padding: 11px 14px;
  border: 1px solid #ced4da;
  border-radius: 7px;
  font-size: 14px;
  outline: none;
}

.search-section input:focus {
  border-color: #6c7ae0;
}

.search-section button {
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
  padding: 15px 18px;
  color: #060708;
  font-size: 13px;
  text-align: left;
  white-space: nowrap;
  border-bottom: 1px solid #dee2e6;
}

td {
  padding: 16px 18px;
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
   STUDENT
========================= */

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
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
   CGPA
========================= */

.cgpa-value {
  font-weight: 700;
  color: #212529;
}


/* =========================
   ACTION
========================= */

.deactivate-button {
  padding: 7px 12px;
  color: #b02a37;
  background: #fff;
  border: 1px solid #dc3545;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.deactivate-button:hover {
  color: white;
  background: #dc3545;
}


/* =========================
   EMPTY STATE
========================= */

.empty-state {
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

.empty-state h3 {
  margin: 0 0 7px;
  color: #343a40;
}

.empty-state p {
  margin: 0;
}


/* =========================
   RESPONSIVE
========================= */

@media (max-width: 700px) {

  .students-page {
    padding: 25px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .student-count {
    width: 100%;
  }

  .search-section {
    flex-direction: column;
  }

  .search-section input {
    max-width: none;
  }

}

</style>