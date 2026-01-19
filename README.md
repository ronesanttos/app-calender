# 📅 App Calender

Sistema web de calendário/agenda com Django, permitindo criar, editar e visualizar eventos, focado em organização, segurança e boa experiência do usuário.

---

## 🚀 Funcionalidades

- Visualização de compromissos em formato de calendário
- Interface interativa com **FullCalendar**
- Autenticação segura utilizando **JWT**
- Persistência de dados com **MongoDB via MongoEngine**
- Organização de compromissos por datas
- Estrutura preparada para integrações e expansões futuras

---

## 📆 Interface de Calendário

 O projeto utiliza FullCalendar.js para exibição dos eventos, permitindo:
 
- Visualização mensal, semanal e diária
- Interação dinâmica com os agendamentos
- Facilidade na criação e edição de eventos

---

## 🔐 Autenticação (JWT)

 A autenticação é baseada em JSON Web Token (JWT), garantindo:

- Segurança nas requisições
- Controle de acesso a rotas protegidas
- Facilidade de integração com front-ends externos ou mobile

---

## 🛠️ Tecnologias Utilizadas

### Back-end
- **Python**
- **Django**
- **MongoEngine**
- **MongoDB**
- **JWT (JSON Web Token)**

### Front-end
- **HTML5**
- **CSS3**
- **JavaScript**
- **FullCalendar.js**

---



## ⚙️ Como Rodar o Projeto Localmente

1. `git clone ...`
2. `cd app-calender`
3. `python -m venv venv`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`

## ⚙️ Configurar variáveis de ambiente (JWT)
- Crie um arquivo .env (ou configure no sistema):

- SECRET_KEY=suachavesecreta
- JWT_SECRET_KEY=sua_chave_jwt
- MONGO_URI=mongodb://localhost:27017/app_calender

## 📂 Estrutura do Projeto
app-calender/
│
├── manage.py
├── requirements.txt
├── project/
│ └── settings.py
├── home/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/
├── base_templates/
├── static/
└── db.sqlite3
