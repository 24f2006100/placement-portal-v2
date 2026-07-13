import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import StudentRegisterView from '../views/StudentRegisterView.vue'
import CompanyRegisterView from '../views/CompanyRegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import CompanyApplicants from '../views/CompanyApplicants.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AdminCompanies from '../views/AdminCompanies.vue'
import AdminStudents from "../views/AdminStudents.vue"
import AdminDrives from '../views/AdminDrives.vue'
import AdminApplications from "../views/AdminApplications.vue"


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/student/register',
      name: 'StudentRegister',
      component: StudentRegisterView
    },
    {
      path: '/company/register',
      name: 'CompanyRegister',
      component: CompanyRegisterView
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: AdminDashboard
    },
    {
      path: '/company/dashboard',
      name: 'CompanyDashboard',
      component: CompanyDashboard
    },
    {
      path: '/student/dashboard',
      name: 'StudentDashboard',
      component: StudentDashboard
    },
    {
    path: "/admin/companies",
    name: "AdminCompanies",
    component: AdminCompanies
    },
    {
    path: "/admin/students",
    name: "AdminStudents",
    component: AdminStudents
    },
    {
    path: "/admin/drives",
    name: "AdminDrives",
    component: AdminDrives
    },
    {
    path: "/admin/applications",
    name: "AdminApplications",
    component: AdminApplications
    },
    {
    path: "/company/applicants/:driveId",
    name: "CompanyApplicants",
    component: CompanyApplicants
    }
  ]  
})

export default router