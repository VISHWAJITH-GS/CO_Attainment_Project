# Faculty Access Guide - CO Attainment Application

**Last Updated:** April 3, 2026

---

## Login Credentials

**Password for ALL accounts:** `tce123`

---

## Faculty by Department

### Computer Science and Engineering (CSE)

| Faculty Name | Email | Employee ID | Status |
|---|---|---|---|
| Dr. S. Mercy Shalinie | `shalinie@tce.edu` | TCE-CSE-1001 | ✅ Active |
| Dr. M. Vijayalakshmi | `mviji@tce.edu` | TCE-CSE-1002 | ✅ Active |
| Dr. M. K. Kavitha Devi | `mkkdit@tce.edu` | TCE-CSE-1003 | ✅ Active |

**Courses Handled:**
- Dr. S. Mercy Shalinie: System Programming, Generative Adversarial Networks, Parallel Computing, Advanced Operating Systems
- Dr. M. Vijayalakshmi: Object Oriented Programming, OOP Lab, Software Project Management, Mobile Application Development
- Dr. M. K. Kavitha Devi: Data Structures and Algorithms, Data Structures Lab, Design and Analysis of Algorithms, Algorithms Lab

---

### Mathematics

| Faculty Name | Email | Employee ID | Status |
|---|---|---|---|
| Dr. B. Vellaikannan | `bvkmat@tce.edu` | TCE-MATH-1001 | ✅ Active |
| Dr. C. S. Senthilkumar | `kumarstays@tce.edu` | TCE-MATH-1002 | ✅ Active |
| Dr. S. P. Suriya Prabha | `suriyaprabha@tce.edu` | TCE-MATH-1003 | ✅ Active |

**Courses Handled:**
- Dr. B. Vellaikannan: Calculus for Engineers, Matrices and Linear Algebra, Numerical Methods, Operations Research
- Dr. C. S. Senthilkumar: Calculus for Engineers, Matrices and Linear Algebra, Probability and Statistics, Discrete Mathematics
- Dr. S. P. Suriya Prabha: Calculus for Engineers, Statistics for Data Science, Linear Algebra for AI, Complex Analysis

---

### Physics

| Faculty Name | Email | Employee ID | Status |
|---|---|---|---|
| Dr. M. Mahendran | `manickam-mahendran@tce.edu` | TCE-PHY-1001 | ✅ Active |
| Dr. N. Sankara Subramanian | `nssphy@tce.edu` | TCE-PHY-1002 | ✅ Active |
| Dr. AL. Subramaniyan | `alsphy@tce.edu` | TCE-PHY-1003 | ✅ Active |

**Courses Handled:**
- Dr. M. Mahendran: Physics, Physics Laboratory, Quantum Mechanics, Solid State Physics
- Dr. N. Sankara Subramanian: Physics, Physics Laboratory, Electromagnetic Waves, Laser Technology
- Dr. AL. Subramaniyan: Physics Laboratory, Engineering Physics, Optics and Fiber Optics, Semiconductor Physics

---

### Chemistry

| Faculty Name | Email | Employee ID | Status |
|---|---|---|---|
| Dr. M. Kottaisamy | `hodchem@tce.edu` | TCE-CHEM-1001 | ✅ Active |
| Dr. V. Velkannan | `velkannan@tce.edu` | TCE-CHEM-1002 | ✅ Active |
| Dr. S. Sivailango | `drssilango@tce.edu` | TCE-CHEM-1003 | ✅ Active |

**Courses Handled:**
- Dr. M. Kottaisamy: Chemistry, Chemistry Laboratory, Environmental Science, Engineering Materials
- Dr. V. Velkannan: Chemistry, Chemistry Laboratory, Water Technology, Polymer Science
- Dr. S. Sivailango: Chemistry, Chemistry Laboratory, Electrochemical Technologies, Spectroscopic Techniques

---

### English

| Faculty Name | Email | Employee ID | Status |
|---|---|---|---|
| Dr. A. Tamilselvi | `tamilselvi@tce.edu` | TCE-ENG-1001 | ✅ Active |
| Dr. S. Rajaram | `sreng@tce.edu` | TCE-ENG-1002 | ✅ Active |
| Dr. G. Jeya Jeevakani | `jeyajeevakani@tce.edu` | TCE-ENG-1003 | ✅ Active |

**Courses Handled:**
- Dr. A. Tamilselvi: Technical English, English Laboratory, Professional Communication, Creative Writing in English
- Dr. S. Rajaram: Technical English, English Laboratory, Professional Communication, Business English
- Dr. G. Jeya Jeevakani: Technical English, English Laboratory, Professional Communication, Soft Skills Development

---

## Quick Login Guide

### From Login Page
1. Visit: `http://127.0.0.1:5173`
2. Enter Faculty Email (from table above)
3. Enter Password: `tce123`
4. Click "Sign In"

### Example Login
```
Email: shalinie@tce.edu
Password: tce123
```

### Features Available After Login
- ✅ Dashboard with assigned subjects
- ✅ Open workspace for each subject
- ✅ Upload question papers and marks files
- ✅ Configure CO parameters
- ✅ View generated reports
- ✅ Download attainment reports
- ✅ Access profile information
- ✅ Change password in settings

---

## Total Faculty Count

| Department | Count |
|---|---|
| Computer Science and Engineering | 3 |
| Mathematics | 3 |
| Physics | 3 |
| Chemistry | 3 |
| English | 3 |
| **TOTAL** | **15** |

---

## System Information

- **Backend:** FastAPI (http://127.0.0.1:8000)
- **Frontend:** React + Vite (http://127.0.0.1:5173)
- **Database:** SQLite (local)
- **Security:** SHA256 password hashing

---

## Troubleshooting

### Login Issues
- **"Invalid credentials"**: Verify email spelling and password is `tce123`
- **"Cannot connect to server"**: Ensure backend is running on port 8000
- **"Page not found"**: Ensure frontend is running on port 5173

### Password Reset
- All faculty can change their password in the Settings page after login
- Current password verification is required for security

---

## Notes for Administrators

- All 15 faculty accounts are pre-configured and active
- Default password is `tce123` for all accounts
- Each faculty has a unique employee ID for tracking
- File uploads are organized by:
  - Email directory (faculty-specific)
  - Subject code subdirectory (subject-specific)
  - This allows secure file isolation and easy sharing

---

**For any issues or additional setup needs, please contact the development team.**
