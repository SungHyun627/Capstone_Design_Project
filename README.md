# Capstone_Design_Project(Pi Reader)

# 1. 설계 배경

![image](https://user-images.githubusercontent.com/62270427/122679111-8d86a800-d224-11eb-9d8d-d3fa19f0ba96.png)![image](https://user-images.githubusercontent.com/62270427/122679079-64feae00-d224-11eb-8afd-74f4c413ca36.png)

- 시력이 좋지 않은 사람의 수가 증가하는 추세이며, 이러한 도와주는 시각 보조 기구의 시장의 규모가 나날이 커지고 있는 상황
- 기존에 있는 text reader 제품은 가격대가 비싸고, user 친화적인 인터페이스를 갖추기 있지 않음
- 기존의 제품이 portable하지 않고 사용법이 복잡하다는 단점이 있음

이를 해결하기 위해, 라즈베리파이를 이용한 대화형 텍스트 reader 기기를 고안


# 2. 하드웨어 아키텍처

% 라즈베리파이 케이스 3D 모델링(Front, Bottom, Top)

![image](https://user-images.githubusercontent.com/62270427/122679615-88c2f380-d226-11eb-9143-fba98484607a.png)  ![image](https://user-images.githubusercontent.com/62270427/122679616-8a8cb700-d226-11eb-8631-41723eaf0ad8.png)  ![image](https://user-images.githubusercontent.com/62270427/122679623-8cef1100-d226-11eb-8b65-602ea53af854.png)

% 사용된 하드웨어 장비
![image](https://user-images.githubusercontent.com/62270427/122680061-7e095e00-d228-11eb-97d9-63f330c252fe.png)

# 3. 소프트웨어 아키텍처

![image](https://user-images.githubusercontent.com/62270427/122680151-d04a7f00-d228-11eb-9066-3872fcf761a4.png)

- Google API : Google STT(오디오 파일을 텍스트로 바꾸는데 변환), Google TTS(사진을 통해 읽은 텍스트를 오디오로 변환), Google Vision API(OCR, image로부터 text를 추출)
- Firebase (Cloud Firestore) : user가 원하는 부분의 페이지를 카테고리별로 저장
- Dialogflow : user의 command(request)를 받아 intent matching을 통하여 적절한 response를 반환
- 그 밖에 사용한 API : 사전 API, 날씨 API

# 4. 전체 아키텍처

![image](https://user-images.githubusercontent.com/62270427/122679985-1b17c700-d228-11eb-9f8c-6e2fff2160cd.png)

# 5. PI Reader
![image](https://user-images.githubusercontent.com/62270427/122680505-70ed6e80-d22a-11eb-83ef-f29d451ef317.png)  ![image](https://user-images.githubusercontent.com/62270427/122680513-764ab900-d22a-11eb-968d-253b67f1636e.png)


# 6. 시연 영상








