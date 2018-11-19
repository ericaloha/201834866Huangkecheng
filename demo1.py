data = {
    "985": ["Yes", "Yes", "No", "No", "Yes", "No", "Yes", "Yes", "No", "Yes"],
    "education": ["bachlor", "bachlor", "master", "master", "bachlor", "master", "master", "phd", "phd", "bachlor"],
    "skill": ["C++", "Java", "Java", "C++", "Java", "C++", "Java", "C++", "Java", "Java"],
    "enrolled": ["No", "Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes", "No"]
}


def read_data(data, cls):
    data_feature = dict()
    data_class = dict()
    for item in data:
        if item != cls:
            data_feature[item] = set(data[item])
        else:
            data_class[item] = set(data[item])

    return data_feature, data_class


def cal_bayes(data, data_feature, data_class):
    p = dict()

    for cls in data_class:
        p[cls] = dict()
        # 计算每个分类的概率 P(C = c1)
        for cls_value in data_class[cls]:
            len_data = len(data[cls])
            len_class = data[cls].count(cls_value)

            # 当前分类的概率
            p_class = len_class / len_data
            p[cls][cls_value] = dict()
            p[cls][cls_value]["p"] = p_class

            # 计算在指定分类下的特征值的条件概率 P(F1 = f11 | C = c1)
            for feature in data_feature:
                pf = p[cls][cls_value]
                pf[feature] = dict()
                for feature_value in data_feature[feature]:
                    count = 0
                    for index in range(len_data):
                        if (data[feature][index] == feature_value and data[cls][index] == cls_value):
                            count += 1
                    pf[feature][feature_value] = round(count / len_data / p_class, 2)
    return p


def predict(p, data):
    cls = p['enrolled']
    result = []

    for item in cls:
        cls_dict = cls[item]
        p_result = cls_dict["p"]
        for key in data:
            p_result *= cls_dict[key][data[key]]
        result.append({
            "name": item,
            "p": p_result
        })

    max = dict({"name": "", "p": 0})
    for item in result:
        if item["p"] > max["p"]:
            max = item

    return max["name"]


if __name__ == "__main__":
    data_feature, data_class = read_data(data, "enrolled")
    p = cal_bayes(data, data_feature, data_class)
    result = predict(p, {
        "985": "Yes",
        "education": "phd",
        "skill": "Java"
    })
    print(result)

    result = predict(p, {
        "985": "Yes",
        "education": "master",
        "skill": "C++"
    })
    print(result)
