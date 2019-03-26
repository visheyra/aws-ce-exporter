import prometheus_client


class Exporter:

    def __init__(self, config):
        self.exposed = {}
        prometheus_client.start_http_server(8000)

    @staticmethod
    def _splat_data(data):
        ret = {}
        for g in data['response'][0]['Groups']:
            svc = g['Keys'][0].replace(' ', '_')
            holder = "{}_unblended_cost".format(svc)
            ret[holder] = g['Metrics']['UnblendedCost']['Amount']

        ret["error_requests_count"] = data['error_request_count']
        ret["success_requests_count"] = data['success_request_count']
        ret["total_requests_count"] = data['error_request_count'] + \
            data['success_request_count']
        return data['metric_labels'], ret

    def create_or_update_counter(self, name, value, meta, job_name):
        labels = ['job_name']
        values = [job_name]
        for k, v in meta.items():
            labels.append(k)
            values.append(v)

        print(labels)
        print(values)
        real_name = name.replace(
            ' ', '_').replace(
                '-', '').replace(
                    '__', '_').lower()
        gauge = None
        try:  # try to get the counter
            gauge = self.exposed[real_name]
        except KeyError:  # the counter does not exist we create it
            gauge = prometheus_client.Gauge(real_name, "", labels)
            self.exposed[real_name] = gauge

        # finally we set the value here
        gauge.labels(*values).set(value)

    def hand_out(self, data):
        meta, splat = Exporter._splat_data(data)

        for k, v in splat.items():
            self.create_or_update_counter(k, v, meta, data['name'])
