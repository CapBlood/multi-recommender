# Pipeline build_recommendations_based_similar

## Overview

Построение рекомендаций на основе близости (похожести) контента.

## Pipeline inputs

- **dataframe** - csv (pandas.Dataframe), на основе которого строятся рекомендации;  
- **target_column** - название целевой колонки (со строковым типом вида `'Tag1, Tag2, Tag3'`) в pandas.Dataframe для построения рекомендаций на основе близости;
- **size** - количество получаемых рекомендаций для каждой строки.

## Pipeline outputs

- **dataframe_with_recs** - csv (pandas.Dataframe) с дополнительной колонкой с рекомендациями.
