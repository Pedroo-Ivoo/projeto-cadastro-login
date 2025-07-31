# Projeto de Cadastro e Login com Flask

## 📄 Descrição

Esta aplicação foi desenvolvida para gerenciar o cadastro e o login de usuários em um sistema. O projeto se concentra em aplicar conhecimentos de backend para garantir a segurança e a validação dos dados, especialmente a proteção de senhas.

- **As funcionalidades principais incluem:**

1. **Cadastro** de usuários com validação de dados.

2. **Login** seguro com autenticação e gerenciamento de sessões.

3. **Consumo da API ViaCEP** para preencher automaticamente o endereço a partir do CEP.

## 🛠️ Tecnologias Utilizadas
A aplicação foi construída com as seguintes tecnologias:

<p align="left">
<a href="https://www.python.org/" target="_blank">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</a>
<a href="https://www.javascript.com/" target="_blank">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</a>
<a href="https://developer.mozilla.org/pt-BR/docs/Web/CSS" target="_blank">
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
</a>
<a href="https://getbootstrap.com/" target="_blank">
<img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
</a>
<a href="https://jquery.com/" target="_blank">
<img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white" alt="jQuery">
</a>
<a href="https://flask.palletsprojects.com/" target="_blank">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
</a>
<a href="https://www.postgresql.org/" target="_blank">
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
</a>
<a href="https://git-scm.com/" target="_blank">
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
</a>
</p>

## 🔐 Funcionalidades e Segurança
Validação de formulários: A validação dos dados de cadastro e login é feita tanto no frontend (com JavaScript e jQuery) quanto no backend (com Flask), garantindo uma camada dupla de segurança. Campos inválidos são destacados visualmente para o usuário.

Segurança de senhas: As senhas são armazenadas no banco de dados em formato de hash, utilizando a biblioteca Bcrypt. Isso impede que as senhas originais sejam expostas, mesmo em caso de vazamento de dados.

Gerenciamento de autenticação: A biblioteca Flask-Login foi utilizada para gerenciar as sessões de usuário, facilitando o controle de acesso às rotas da aplicação de forma segura e eficiente, sem a necessidade de criar uma lógica própria.

## 🚀 Melhorias Futuras
O projeto já funciona bem, mas há planos para aprimoramentos, como:

1. **Validação de senhas mais robusta:** Adicionar a obrigatoriedade de caracteres maiúsculos e números nas senhas.

2. **Recuperação de senha:** Implementar um fluxo seguro de recuperação de senha utilizando tokens de autenticação.

3. **Sistema de hierarquia de acesso:** Criar diferentes níveis de permissão (administrador, usuário, convidado) para controlar o acesso a certas funcionalidades da aplicação.

4. **Deleção de cadastro:** Criar metodo de exclusão do cadastros existentes.