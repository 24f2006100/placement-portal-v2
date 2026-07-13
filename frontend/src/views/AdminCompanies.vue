<template>
  <div>
    <Navbar />

    <main class="companies-page">

      <!-- PAGE HEADER -->
      <div class="page-header">
        <div>
          <p class="page-label">ADMIN MANAGEMENT</p>
          <h1>Registered Companies</h1>
          <p class="page-description">
            Search, review and manage companies registered on the portal.
          </p>
        </div>

        <div class="company-count">
          <span>Total Companies</span>
          <strong>{{ companies.length }}</strong>
        </div>
      </div>


      <!-- SEARCH -->
      <div class="search-section">

        <input
          v-model="searchName"
          type="text"
          placeholder="Search company by name..."
          @keyup.enter="searchCompanies"
        />

        <button
          class="search-button"
          @click="searchCompanies"
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


      <!-- EMPTY STATE -->
      <div
        v-if="companies.length === 0"
        class="empty-state"
      >
        No companies found.
      </div>


      <!-- COMPANY TABLE -->
      <div
        v-else
        class="table-card"
      >

        <div class="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Company</th>
                <th>HR Name</th>
                <th>Email</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="company in companies"
                :key="company.id"
              >

                <!-- COMPANY -->
                <td>
                  <div class="company-info">

                    <div class="company-avatar">
                      {{
                        company.company_name
                          ? company.company_name
                              .charAt(0)
                              .toUpperCase()
                          : "C"
                      }}
                    </div>

                    <strong>
                      {{ company.company_name }}
                    </strong>

                  </div>
                </td>


                <!-- HR NAME -->
                <td>
                  {{ company.hr_name || "Not Provided" }}
                </td>


                <!-- EMAIL -->
                <td>
                  {{ company.email }}
                </td>


                <!-- STATUS -->
                <td>

                  <span
                    class="status-badge"
                    :class="
                      company.approval_status
                        ?.toLowerCase()
                    "
                  >
                    {{ company.approval_status }}
                  </span>

                </td>


                <!-- ACTIONS -->
                <td>

                  <div class="action-buttons">

                    <button
                      v-if="
                        company.approval_status ===
                        'Pending'
                      "
                      class="approve-button"
                      @click="
                        approveCompany(company.id)
                      "
                    >
                      Approve
                    </button>


                    <button
                      v-if="
                        company.approval_status ===
                        'Pending'
                      "
                      class="reject-button"
                      @click="
                        rejectCompany(company.id)
                      "
                    >
                      Reject
                    </button>


                    <span
                      v-if="
                        company.approval_status !==
                        'Pending'
                      "
                      class="processed-text"
                    >
                      Processed
                    </span>


                    <button
                        v-if="company.is_active"
                        @click="deactivateCompany(company.id)"
                        >
                        Deactivate
                        </button>

                        <button
                        v-else
                        disabled
                        >
                        Deactivated
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

import { ref, onMounted } from "vue"

import Navbar from "../components/Navbar.vue"
import api from "../services/api"


const companies = ref([])
const searchName = ref("")


// =====================================
// LOAD COMPANIES
// =====================================

async function loadCompanies() {

  try {

    const response = await api.get(
      "/admin/companies"
    )

    companies.value = response.data

  } catch (error) {

    console.log(error)

  }

}


// =====================================
// SEARCH COMPANIES
// =====================================

async function searchCompanies() {

  try {

    if (!searchName.value.trim()) {

      await loadCompanies()

      return

    }


    const response = await api.get(
      "/admin/search/company",
      {
        params: {
          name: searchName.value
        }
      }
    )


    companies.value = response.data

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to search companies"
    )

  }

}


// =====================================
// CLEAR SEARCH
// =====================================

async function clearSearch() {

  searchName.value = ""

  await loadCompanies()

}


// =====================================
// APPROVE COMPANY
// =====================================

async function approveCompany(id) {

  try {

    const response = await api.put(
      `/admin/company/${id}/approve`
    )

    alert(
      response.data.message ||
      "Company approved successfully"
    )

    await loadCompanies()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to approve company"
    )

  }

}


// =====================================
// REJECT COMPANY
// =====================================

async function rejectCompany(id) {

  try {

    const response = await api.put(
      `/admin/company/${id}/reject`
    )

    alert(
      response.data.message ||
      "Company rejected successfully"
    )

    await loadCompanies()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to reject company"
    )

  }

}


// =====================================
// DEACTIVATE COMPANY
// =====================================

async function deactivateCompany(id) {

  const confirmed = confirm(
    "Are you sure you want to deactivate this company?"
  )


  if (!confirmed) return


  try {

    const response = await api.put(
      `/admin/company/${id}/deactivate`
    )


    alert(response.data.message)


    await loadCompanies()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Failed to deactivate company"
    )

  }

}


onMounted(loadCompanies)

</script>


<style scoped>

.companies-page {
  max-width: 1250px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}


/* PAGE HEADER */

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


/* COMPANY COUNT */

.company-count {
  min-width: 150px;
  padding: 16px 22px;
  text-align: center;
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.company-count span {
  display: block;
  margin-bottom: 4px;
  color: #6c757d;
  font-size: 13px;
}

.company-count strong {
  color: #212529;
  font-size: 26px;
}


/* SEARCH */

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


/* TABLE CARD */

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
  border-bottom: 1px solid #dee2e6;
}

td {
  padding: 16px 18px;
  color: #495057;
  font-size: 14px;
  border-bottom: 1px solid #eeeeee;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover {
  background: #fafbfc;
}


/* COMPANY */

.company-info {
  display: flex;
  align-items: center;
  gap: 12px;
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


/* STATUS */

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


/* ACTIONS */

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

.deactivate-button {
  color: #495057;
  background: white;
  border: 1px solid #adb5bd;
}

.processed-text {
  color: #6c757d;
  font-size: 12px;
}


/* EMPTY */

.empty-state {
  padding: 50px;
  text-align: center;
  color: #6c757d;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}


/* RESPONSIVE */

@media (max-width: 700px) {

  .companies-page {
    padding: 25px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .company-count {
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