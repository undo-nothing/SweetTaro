import datetime
import functools
import os
import pickle
import time

from .term_color import colored


def time_it(method):
    """time_it
    t_start - t_end = used_time

    you can offer a dict to store the timing result

    example:
    log_time_container = {}
    result = SomeClass.get_all_result(log_time=log_time_container)

    :param method: callable
    :return:
    """
    @functools.wraps(method)
    def timed(*args, **kw):
        t_start = time.time()
        result = method(*args, **kw)
        t_end = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((t_end - t_start) * 1000)
        else:
            print('\n# ' +
                  colored('--- {: >10.5f} ms --- {!r}'.format(
                      (t_end - t_start) * 1000, method.__name__), 'green'))
        return result

    return timed


def pickle_post_cdata(method):
    """pickle_post_cdata
    """
    @functools.wraps(method)
    def wraps_func(*args, **kw):
        request = args[0]
        if request.method == 'POST':
            url = request.get_full_path()
            query_params = request.GET.dict()
            raw_data = request.body
            sn = query_params.get('SN')
            file_path = './device/%s/%s_' % (sn, sn) + datetime.datetime.now().strftime('%Y%m%d%H%M%S.pk')
            if not os.path.exists(os.path.split(file_path)[0]):
                os.makedirs(os.path.split(file_path)[0])

            with open(file_path, 'wb') as f:
                pickle.dump((url, query_params, raw_data), f)
        else:
            # print('GET')
            pass
        result = method(*args, **kw)
        return result

    return wraps_func


def request_monitor(method):
    """request_monitor
    """
    @functools.wraps(method)
    def wraps_func(*args, **kw):
        request = args[0]
        if True:
            print('##################### request_monitor ##########################')
            print('url--------------', request.path)
            print('method-----------', request.method)
            print('query_params ----', dict(request.GET))
            print('raw_body_data----', request.body)
            print('################################################################')

        return method(*args, **kw)

    return wraps_func
