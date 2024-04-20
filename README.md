# Descrição

Projeto para a ativação remota de uma bomba de água para pequenas plantas

# Composição do projeto

## control_server

Servidor escrito em django para controlar a bomba via interface web. Contém autenticação. Crie usuários utilizando a interface admin do django

### Instalando

Use o script install_dependencies.sh. Ele irá instalar as dependências
do python, criar a base sqlite inicial, pedir a criação de um superusuário, 
além de criar um serviço de startup para o servidor

IMPORTANTE: Para acesso em rede interna, é necessário liberar a porta
8000 para acesso externo. Recomenda-se o uso do utilitário firewall-config
(Instalável via apt-get).

Para fazer as alterações no firewall permanentes, mude em Options/Runtime to 
permanent

## arduino_pump_control

Firmware da placa arduino que de fato controla a bomba
