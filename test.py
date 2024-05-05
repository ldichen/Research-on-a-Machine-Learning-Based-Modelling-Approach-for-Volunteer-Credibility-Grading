import pandas as pd

path = "D:\\Desktop\\data\\isChina\\notNull\\ChinaData\\concat\\"
# 读取CSV文件到DataFrame
df = pd.read_csv('D:\\Desktop\\concatAll.csv')

# 删除指定列  'Unnamed: 0.1', 'Unnamed: 0', 'create_by', 'created by'   'description'
# 'Unnamed: 0.1','Unnamed: 0','bundle_id','build','ideditor:walkthrough_completed','ideditor:walkthrough_progress','ideditor:walkthrough_started'
# 'build','host','created_by:library','resolved:mismatched_geometry:vertex_as_point','resolved:help_request:fixme_tag','resolved:outdated_tags:deprecated_tags','resolved:crossing_ways:building-building','warnings:close_nodes:vertices','resolved:close_nodes:vertices','resolved:outdated_tags:noncanonical_brand','warnings:crossing_ways:building-building','warnings:disconnected_way:highway','resolved:almost_junction:highway-highway','mapwithai','warnings:crossing_ways:building-highway','mapwithai:options','warnings:crossing_ways:highway-highway','resolved:outdated_tags:incomplete_tags','warnings:crossing_ways:highway-waterway','warnings:almost_junction:highway-highway'
# columns_to_drop = ['locale','warnings:disconnected_way','resolved:crossing_ways:building-highway','resolved:crossing_ways:highway-highway','resolved:disconnected_way:highway','warnings:outdated_tags:deprecated_tags','tag','warnings:help_request:fixme_tag','warnings:outdated_tags:incomplete_tags','warnings:outdated_tags:noncanonical_brand','closed:note','resolved:mismatched_geometry:point_as_vertex','import','source:date','url','resolved:crossing_ways:highway-railway','resolved:suspicious_name:generic_name','os','resolved:missing_tag:any','warnings:impossible_oneway:highway','']  # 要删除的列名列表
# 指定需要保留的列名列表
columns_to_keep = ['id', 'created_at', 'closed_at', 'open', 'user', 'uid', 'min_lat', 'min_lon', 'max_lat', 'max_lon',
                   'num_changes', 'comments_count', 'comment', 'created_by', 'centerLon', 'centerLat', 'isChina',
                   'version', 'source', 'bot', 'hashtags', 'changesets_count', 'imagery_used', 'review_requested',
                   'StreetComplete:quest_type']

# 删除除了指定列之外的所有列
df = df[columns_to_keep]

# 将修改后的DataFrame保存回CSV文件
df.to_csv('D:\\Desktop\\concatAll2.csv', index=False)
# df = df.drop(columns=columns_to_drop)

# 将所有空值设置为0
# df = df.fillna(0)

# 将修改后的DataFrame保存回CSV文件
# df.to_csv('D:\\Desktop\\concatAll.csv', index=False)
