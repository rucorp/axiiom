# UniveriD Project - Complete Structure and Information

## Project Overview
- **Name**: UniveriD - Цифровая студенческая жизнь
- **Domain**: univerid.mobiap.com
- **Description**: Educational platform that unifies student ID, access pass, schedule, and services in one application
- **Focus**: Universities and colleges in St. Petersburg, Russia

## Project Architecture

### Main Files
- `index.html` - Main landing page
- `README.md` - Project documentation
- `CNAME` - Custom domain configuration
- `create_university_pages.py` - Script to generate university pages
- `template.html` - Template for university pages

### Page Structure
- `about.html` - About the project
- `abiturients.html` - Information for prospective students
- `alumni.html` - Alumni resources
- `benefits.html` - Benefits offered
- `career.html` - Career services
- `demo.html` - Interactive demonstration
- `ecology.html` - Environmental programs
- `features.html` - Feature descriptions
- `for-universities.html` - University partnership info
- `housing.html` - Student accommodation
- `partners.html` - Partner information
- `science.html` - Research programs
- `support.html` - Support resources
- `universities.html` - List of partner universities
- `universities1.html` - Additional universities info

### Assets
- `/styles/` - CSS files
  - `demo.css`
  - `features.css`
  - `home.css`
  - `main.css`
  - `page.css`
- `/js/` - JavaScript files
  - `main.js` - Main JavaScript functionality

## University Pages
The project includes individual pages for 70+ educational institutions in St. Petersburg:

### Universities
- СПбГУ (Saint Petersburg State University)
- СПбПУ/Политех (Saint Petersburg Polytechnic University)
- НИУ ВШЭ Санкт-Петербург (Higher School of Economics)
- РГПУ им. А.И. Герцена (Herzen University)
- СПбГМУ им. Павлова (Pavlov First Saint Petersburg State Medical University)
- СПбГЭУ/ФинЭк (Saint Petersburg State University of Economics)
- Европейский университет в Санкт-Петербурге (European University)
- Санкт-Петербургский филиал РАНХиГС (RANEPA)
- Many others...

### Institutes
- Военмех им. Д.Ф. Устинова (Military Mechanical Engineering Institute)
- СПбГЭТУ ЛЭТИ (Saint Petersburg Electrotechnical University)
- СПбГИК (Saint Petersburg State Institute of Cinema and Television)
- СПбГИТМО (Saint Petersburg National Research University of Information Technologies, Mechanics and Optics)
- Many others...

### Colleges (Колледжи)
- Петровский колледж
- КИП колледж информатики и программирования
- Петербургский колледж связи 54
- Колледж Санкт-Петербург
- Политехнический колледж 31
- Медицинский колледж 1
- And many more specialized colleges...

## Technical Features
- HTML5, CSS3, JavaScript frontend
- Responsive design for mobile and desktop
- SEO-friendly structure
- Dark/light theme toggle
- Modern UI with accessibility features
- University card linking system
- Generated university pages with standardized content

## Functionality
- The Python script `create_university_pages.py`:
  - Generates individual pages for each university using a template
  - Creates SEO-friendly URLs using slugification
  - Updates the universities.html page to make all university cards clickable links
  - Includes structured content for each institution with sections for:
    - About the institution
    - Contacts
    - Student resources
    - Admissions information
    - Alumni information

## Project Purpose
UniveriD aims to create a unified digital platform for student life in St. Petersburg universities, providing:
- Digital student ID
- Access control
- Schedule management
- University services
- Resource access

## Deployment
- Designed for GitHub Pages deployment
- Custom domain configured
- Static file hosting compatible