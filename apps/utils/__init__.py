

def model_bulk_create(datas, model_cls, bulk_size=2000):
    for i in range(len(datas) // bulk_size + 1):
        model_cls.objects.bulk_create(datas[i * bulk_size: (i + 1) * bulk_size])
