# chinese_to_arabic.py

def chinese2arabic(chinese_number):
    """
    将中文数字转换为阿拉伯数字。
    
    参数:
        chinese_number (str): 中文数字字符串，例如 "一百二十三"。
        
    返回:
        int: 转换后的阿拉伯数字。
        
    异常:
        ValueError: 如果输入包含无效的中文字符。
    """
    # 定义中文数字与阿拉伯数字的映射关系
    chinese_num_map = {
        '零': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
    }
    
    # 定义中文单位与对应倍数的映射关系
    chinese_unit_map = {
        '十': 10,
        '百': 100,
        '千': 1000,
        '万': 10000,
        '亿': 100000000,
    }
    
    result = 0
    temp = 0
    for char in chinese_number:
        if char in chinese_num_map:
            temp = chinese_num_map[char]
        elif char in chinese_unit_map:
            # 如果遇到单位，将临时结果乘以单位倍数并加到最终结果中
            if char == '十' and temp == 0:
                temp = 1
            result += temp * chinese_unit_map[char]
            temp = 0
        else:
            raise ValueError(f"无效的中文字符: {char}")
    
    # 加上最后的临时结果
    result += temp
    
    return result
