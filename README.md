# 한국어 데이터 파이프라인(data-pipeline-korean)
일반적으로 잘 알려진 벤치마크 데이터셋에 대하여 모델 학습, 임베딩, 사전 학습을 위한 한국어 데이터 정제 방법을 구현하였습니다.

## 구현 방법 및 범위
해당 repository는 한국어 위키 백과(kowiki), 나무 위키(namu wiki), KorQuAD 1.0, KorQuAD 2.1 데이터셋을 파싱(parsing)하고 목적에 맞게 다듬기 위한 코드를 제공하고 있습니다.

- 적용가능 데이터: 한국어 위키 백과(kowiki), 나무 위키(namu wiki), KorQuAD 1.0, KorQuAD 2.1
- 구현 기능: 문장 추출, 원본 데이터 추출(예정), 각 과제에 맞는 데이터셋 구축(예정)

## 실행방법
extract_sentences.py: 데이터에서 한국어 문장을 추출하는 코드.
```
extract_sentences.py --input_dir <input file directory> --output_dir <output file directory> --prefix sentences_ --data_type kowiki-sens-kor --num_cores 16
``` 
- input_dir: 입력 파일의 폴더 경로를 설정합니다.
- output_dir: 출력 파일의 폴더 경로를 설정합니다.
- prefix: 출력 파일의 이름 앞에 추가될 접두사를 설정합니다.
- data_type: 입력 데이터의 유형을 설정합니다(현재 지원되는 유형: 'korquad1-sens-kor', 'korquad2-sens-kor', 'kowiki-sens-kor', 'namuwiki-sens-kor').
- num_cores: multiprocessing에서 이용할 cpu코어의 개수를 설정합니다.


## 기타 및 유의사항
- 해당 코드에 의해 추출된 문장들은 주로 단어장 생성, 사전 학습을 위한 코드입니다.
- kowiki의 경우 multiprocessing 이 적용되지 않습니다.
- 이외에도 추가 기능들이 추후에 업데이트 될 예정입니다.
