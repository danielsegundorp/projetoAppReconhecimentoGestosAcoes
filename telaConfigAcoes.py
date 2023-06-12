import cv2
import mediapipe as mp
import psycopg2 as pg2
from psycopg2 import Error


def configAcoes(id_usuario):
    print("\n")
    print("CONFIGURAÇÂO AÇÕES -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|")
    

    # Configurações de conexão com o banco de dados
    db_host = 'localhost'
    db_port = 5432
    db_name = 'projetoB2'
    db_user = 'postgres'
    db_password = 'password'

    # Inicializa funcionalidades mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                            max_num_hands=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)

    # Inicializa video
    cap = cv2.VideoCapture(0)

    # Conexão com o banco
    try:
        conn = pg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        def get_action_messages(id_usuario):
            # Consulta o banco de dados para todas as mensagens
            query = "SELECT nome, descricao FROM acoes WHERE usuarioid = %s"
            cursor.execute(query, (id_usuario,))
            results = cursor.fetchall()

            action_messages = {action: message for action, message in results}

            return action_messages

        def insert_action_message(id_usuario, action, message):
            # Verifica se já existe uma ação cadastrada
            check_query = "SELECT COUNT(*) FROM acoes WHERE nome = %s AND usuarioid = %s"
            cursor.execute(check_query, (action, id_usuario))
            count = cursor.fetchone()[0]
            if count > 0:
                print("Registro não permitido, já existe uma ação com esse nome.")
            else:
                # Insere novas mensagens da ação
                insert_query = "INSERT INTO acoes (usuarioid, acoes_id, nome, descricao) VALUES (%s, DEFAULT, %s, %s)"
                cursor.execute(insert_query, (id_usuario, action, message))
                conn.commit()
                print("Mensagem da ação inserida com sucesso!")

        def update_action_message(id_usuario, action, message):
            # Atualiza as mensagens existentes
            update_query = "UPDATE acoes SET descricao = %s WHERE nome = %s AND usuarioid = %s"
            cursor.execute(update_query, (message, action, id_usuario))
            conn.commit()
            print("Mensagem da ação atualizada com sucesso!")


        def delete_action(id_usuario, action):
            # Apaga as mensagens juntamente com a ação do usuário específico
            delete_query = "DELETE FROM acoes WHERE nome = %s AND usuarioid = %s"
            cursor.execute(delete_query, (action, id_usuario))
            conn.commit()
            print("Ação apagado com sucesso!")


        def delete_action_message(id_usuario, action):
            # Apaga somente as mensagens e mantém o nome da ação do usuário específico
            delete_query = "UPDATE acoes SET descricao = NULL WHERE nome = %s AND usuarioid = %s"
            cursor.execute(delete_query, (action, id_usuario))
            conn.commit()
            print("Mensagem da ação apagada com sucesso!")


        def recognize_action(action_messages):
            while True:
                # Leitura da camera
                ret, frame = cap.read()

                # Vira a moldura horizontalmente para um efeito de espelho
                frame = cv2.flip(frame, 1)

                # Converte a imagem BGR para RGB
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Processa a imagem com o modulo mediapipe
                results = hands.process(rgb)

                # Limpa a tela do terminal
                print("\033c", end='')

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # obtem os pontos de referencia para cada mão
                        landmarks = []
                        for index, landmark in enumerate(hand_landmarks.landmark):
                            landmarks.append((index, (landmark.x, landmark.y, landmark.z)))

                        # Executar o reconhecimento de gestos
                        thumb_tip = landmarks[4][1]
                        index_finger_tip = landmarks[8][1]

                        # Mostra uma ação pelo gesto positivo
                        if thumb_tip[1] < index_finger_tip[1]:
                            action = 'positivo'
                        # Mostra uma ação pelo gesto do polegar joia
                        elif landmarks[6][1][0] < thumb_tip[0] and landmarks[10][1][0] > index_finger_tip[0]:
                            action = 'vitoria'
                        # Mostra uma ação pelo gesto do polegar joia para baixo
                        elif landmarks[4][1][1] > landmarks[3][1][1] and landmarks[4][1][1] > landmarks[2][1][1]:
                            action = 'negativo'
                        # Mostra uma ação pelo gesto com as mãos abertas
                        elif landmarks[4][1][1] < landmarks[3][1][1] and landmarks[4][1][1] < landmarks[2][1][1]:
                            action = 'olamundo'
                        else:
                            action = 'none'

                        # Recupera a mensagem de gesto do dicionário
                        message = action_messages.get(action)

                        if message:
                            print(message)
                        else:
                            print("Nenhuma ação encontrada.")

                        # Desenha os pontos de referência da imagem
                        for _, point in landmarks:
                            x, y = int(point[0] * frame.shape[1]), int(point[1] * frame.shape[0])
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                        # Desenha as linhas de referência
                        connections = mp_hands.HAND_CONNECTIONS
                        for connection in connections:
                            point1 = landmarks[connection[0]][1]
                            point2 = landmarks[connection[1]][1]
                            x1, y1 = int(point1[0] * frame.shape[1]), int(point1[1] * frame.shape[0])
                            x2, y2 = int(point2[0] * frame.shape[1]), int(point2[1] * frame.shape[0])
                            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                else:
                    print("Nenhum gesto detectado.")

                # mensagem do quadro da camera
                cv2.imshow('Reconhecimento de Gestos', frame)

                # Fecha a camera ao pressionar q do teclado
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

           
            cap.release()
            cv2.destroyAllWindows()

        def print_available_action(action_messages):
            if not action_messages:
                print("Nenhuma ação disponível.")
            else:
                print("Ações Disponíveis:")
                for action, message in action_messages.items():
                    print(f"{action}: {message}")

        def show_unregistered_action(action_messages):
            unregistered_action = [action for action, message in action_messages.items() if not message]
            if unregistered_action:
                print("Ações sem mensagens registradas:")
                for action in unregistered_action:
                    print(action)
            else:
                print("Todos as ações já possuem mensagens registradas.!")

        def close_camera():
            cap.release()
            cv2.destroyAllWindows()

       
        while True:
            print("\nMenu:")
            print("1. Registrar uma nova mensagem de ação")
            print("2. Atualizar uma mensagem de ação existente")
            print("3. Apagar ação e a mensagem")
            print("4. Apagar a mensagem da ação")
            print("5. Iniciar reconhecimento")
            print("6. Mostrar ações disponíveis")
            print("7. Mostrar ações sem funções registradas")
            print("0. Sair")

            choice = input("Escolha uma opção: ")

            if choice == '1':
                action = input("Digite o nome da ação: ")
                message = input("Digite a mensagem da ação: ")
                insert_action_message(id_usuario, action, message)

            elif choice == '2':
                action_messages = get_action_messages(id_usuario)
                print_available_action(action_messages)
                action = input("Digite o nome da ação para atualizar: ")
                if action in action_messages:
                    message = input("Digite a mensagem da ação para atualizar: ")
                    update_action_message(id_usuario, action, message)
                else:
                    print("Ação não encontrada.!")

            elif choice == '3':
                action_messages = get_action_messages(id_usuario)
                print_available_action(action_messages)
                action = input("Digite o nome da ação para apagar: ")
                if action in action_messages:
                    delete_action(id_usuario, action)
                else:
                    print("Ação não encontrada.!")

            elif choice == '4':
                gesture_messages = get_action_messages(id_usuario)
                print_available_action(action_messages)
                action = input("Digite o nome da ação para apagar a mensagem: ")
                if action in gesture_messages:
                    delete_action_message(id_usuario, action)
                else:
                    print("Ação não encontrada.!")

            elif choice == '5':
                action_messages = get_action_messages(id_usuario)
                recognize_action(action_messages)

            elif choice == '6':
                action_messages = get_action_messages(id_usuario)
                print_available_action(action_messages)

            elif choice == '7':
                action_messages = get_action_messages(id_usuario)
                show_unregistered_action(action_messages)

            elif choice == '0':
                break

    except Error as e:
        print("Erro ao conectar com o banco de dados:", e)

    finally:
        close_camera()
        if conn:
            cursor.close()
            conn.close()
            print("Menu Ações Fechado.")