import pandas as pd
def adjust_annotations_csv(file_path):
    file_path_result = file_path.split('/')[1]
    annotations = pd.read_csv(file_path, names = ['image_name', 'Left', 'Upper', 'Right', 'Lower', 'label'])
    encode = {'narmal': 0, 'Shoplifting': 1}
    annotations['label'] = annotations['label'].apply(lambda x: 0 if x=='normal' else 1)
    annotations['image_name'] = annotations.index.map(lambda x: str(x) + '.jpg')
    result_file_name = 'annotations_' + file_path_result + '.csv'
    annotations.to_csv(result_file_name, index=False)
adjust_annotations_csv('project/train/_annotations.csv')
adjust_annotations_csv('project/test/_annotations.csv')  
adjust_annotations_csv('project/valid/_annotations.csv')
