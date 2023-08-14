Nova versão do servidor de chat com as seguintes melhorias solicitadas:

O servidor agora utiliza threads para lidar com as conexões dos clientes, melhorando a escalabilidade.
O cadastro de usuários é armazenado no dicionário registry, com acesso controlado por um bloqueio (registry_lock) para garantir a consistência dos dados.
A função get_user_address é usada para obter o endereço (IP e porta) de um usuário a partir do cadastro.
A função get_user_port é usada para obter apenas o número da porta de um usuário.
A função send_message é usada para enviar mensagens para um usuário específico, utilizando o cadastro para encontrar o endereço correto.
O servidor utiliza threads para tratar as conexões dos clientes, permitindo que ele lide com várias conexões simultaneamente.