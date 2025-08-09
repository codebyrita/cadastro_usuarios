# 📋 Sistema de Cadastro de Usuários

![Flask](https://img.shields.io/badge/Flask-2.0+-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

Sistema web desenvolvido em **Flask** para gerenciamento de usuários, com CRUD completo (criar, listar, editar e excluir), validação de senha, prevenção de e-mails duplicados e interface responsiva.

## 🚀 Funcionalidades
- Cadastro de usuários com validação de campos obrigatórios
- Validação de senha forte (6 a 8 caracteres, maiúscula, minúscula, número e símbolo)
- Prevenção de cadastro com e-mail duplicado
- Edição e exclusão de registros
- Listagem paginada de usuários
- Mensagens de sucesso e erro automáticas (Flash)
- Interface responsiva usando **Bootstrap 5**

---

## 🖼️ Screenshots

### Página de Cadastro
![Cadastro](docs/img/cadastro.png)

### Lista de Usuários
![Lista](docs/img/lista.png)

### Página de Edição
![Edição](docs/img/editar.png)

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Flask**
- **SQLite**
- **Bootstrap 5**
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**

---

## 📦 Como instalar e executar

```bash
# Clone este repositório
git clone https://github.com/SEU-USUARIO/cadastro_usuarios.git

# Entre na pasta
cd cadastro_usuarios

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py

Sistema disponível neste endereco:
http://127.0.0.1:5000
