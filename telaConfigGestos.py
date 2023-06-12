import cv2
import mediapipe as mp
import psycopg2 as pg2
from psycopg2 import Error


def configGestos(id_usuario):
    print("\n")
    print("CONFIGURAÇÂO GESTOS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|")
    

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

        def get_gesture_messages(id_usuario):
            # Consulta o banco de dados para todas as mensagens de gesto
            query = "SELECT nome, descricao FROM gestos WHERE usuarioid = %s"
            cursor.execute(query, (id_usuario,))
            results = cursor.fetchall()

            gesture_messages = {gesture: message for gesture, message in results}

            return gesture_messages

        def insert_gesture_message(id_usuario, gesture, message):
            # Verifica se o gesto já existe
            check_query = "SELECT COUNT(*) FROM gestos WHERE nome = %s AND usuarioid = %s"
            cursor.execute(check_query, (gesture, id_usuario))
            count = cursor.fetchone()[0]
            if count > 0:
                print("Registro não permitido, já existe um gesto com esse nome.")
            else:
                # Insere novas mensagens de gesto
                insert_query = "INSERT INTO gestos (usuarioid, gestos_id, nome, descricao) VALUES (%s, DEFAULT, %s, %s)"
                cursor.execute(insert_query, (id_usuario, gesture, message))
                conn.commit()
                print("Mensagem do gesto inserida com sucesso!")

        def update_gesture_message(id_usuario, gesture, message):
            # Atualiza as mensagens existentes
            update_query = "UPDATE gestos SET descricao = %s WHERE nome = %s AND usuarioid = %s"
            cursor.execute(update_query, (message, gesture, id_usuario))
            conn.commit()
            print("Mensagem do gesto atualizada com sucesso!")


        def delete_gesture(id_usuario, gesture):
            # Apaga as mensagens juntamente com o gesto do usuário específico
            delete_query = "DELETE FROM gestos WHERE nome = %s AND usuarioid = %s"
            cursor.execute(delete_query, (gesture, id_usuario))
            conn.commit()
            print("Gesto apagado com sucesso!")


        def delete_gesture_message(id_usuario, gesture):
            # Apaga somente as mensagens e mantém o nome do gesto do usuário específico
            delete_query = "UPDATE gestos SET descricao = NULL WHERE nome = %s AND usuarioid = %s"
            cursor.execute(delete_query, (gesture, id_usuario))
            conn.commit()
            print("Mensagem do gesto apagada com sucesso!")


        def recognize_gesture(gesture_messages):
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

                       
                        thumb_tip = landmarks[4][1]
                        index_finger_tip = landmarks[8][1]

                    
                        if thumb_tip[1] < index_finger_tip[1]:
                            gesture = 'positivo'
                        
                        elif landmarks[6][1][0] < thumb_tip[0] and landmarks[10][1][0] > index_finger_tip[0]:
                            gesture = 'vitoria'
                        
                        elif landmarks[4][1][1] > landmarks[3][1][1] and landmarks[4][1][1] > landmarks[2][1][1]:
                            gesture = 'negativo'
                        
                        elif landmarks[4][1][1] < landmarks[3][1][1] and landmarks[4][1][1] < landmarks[2][1][1]:
                            gesture = 'olamundo'
                        else:
                            gesture = 'none'

            
                        message = gesture_messages.get(gesture)

                        if message:
                            print(message)
                        else:
                            print("Nenhum gesto encontrado.")

                       
                        for _, point in landmarks:
                            x, y = int(point[0] * frame.shape[1]), int(point[1] * frame.shape[0])
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                        
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

        def print_available_gestures(gesture_messages):
            if not gesture_messages:
                print("Nenhum gesto disponível.")
            else:
                print("Gestos Disponíveis:")
                for gesture, message in gesture_messages.items():
                    print(f"{gesture}: {message}")

        def show_unregistered_gestures(gesture_messages):
            unregistered_gestures = [gesture for gesture, message in gesture_messages.items() if not message]
            if unregistered_gestures:
                print("Gestos sem mensagens registradas:")
                for gesture in unregistered_gestures:
                    print(gesture)
            else:
                print("Todos os gestos já possuem mensagens registradas.!")

        def close_camera():
            cap.release()
            cv2.destroyAllWindows()

       
        while True:
            print("\nMenu:")
            print("1. Registrar uma nova mensagem de gesto")
            print("2. Atualizar uma mensagem de gesto existente")
            print("3. Apagar o gesto e a mensagem")
            print("4. Apagar a mensagem do gesto")
            print("5. Iniciar reconhecimento de gesto")
            print("6. Mostrar gestos disponíveis")
            print("7. Mostrar gestos sem mensagens registradas")
            print("0. Sair")

            choice = input("Escolha uma opção: ")

            if choice == '1':
                gesture = input("Digite o nome do gesto: ")
                message = input("Digite a mensagem do gesto: ")
                insert_gesture_message(id_usuario, gesture, message)

            elif choice == '2':
                gesture_messages = get_gesture_messages(id_usuario)
                print_available_gestures(gesture_messages)
                gesture = input("Digite o nome do gesto para atualizar: ")
                if gesture in gesture_messages:
                    message = input("Digite a mensagem do gesto para atualizar: ")
                    update_gesture_message(id_usuario, gesture, message)
                else:
                    print("Gesto não encontrado.!")

            elif choice == '3':
                gesture_messages = get_gesture_messages(id_usuario)
                print_available_gestures(gesture_messages)
                gesture = input("Digite o nome do gesto para apagar: ")
                if gesture in gesture_messages:
                    delete_gesture(id_usuario, gesture)
                else:
                    print("Gesto não encontrado.!")

            elif choice == '4':
                gesture_messages = get_gesture_messages(id_usuario)
                print_available_gestures(gesture_messages)
                gesture = input("Digite o nome do gesto para apagar a mensagem: ")
                if gesture in gesture_messages:
                    delete_gesture_message(id_usuario, gesture)
                else:
                    print("Gesto não encontrado!")

            elif choice == '5':
                gesture_messages = get_gesture_messages(id_usuario)
                recognize_gesture(gesture_messages)

            elif choice == '6':
                gesture_messages = get_gesture_messages(id_usuario)
                print_available_gestures(gesture_messages)

            elif choice == '7':
                gesture_messages = get_gesture_messages(id_usuario)
                show_unregistered_gestures(gesture_messages)

            elif choice == '0':
                break

    except Error as e:
        print("Erro ao conectar com o banco de dados:", e)

    finally:
        close_camera()
        if conn:
            cursor.close()
            conn.close()
            print("Menu Gesto Fechado.")