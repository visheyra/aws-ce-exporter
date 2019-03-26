import boto3


class CostExplorerJob:

    def __init__(self, labels, credentials, name, metrics,
                 granularity, start, end, refresh=5):
        print('im generated')
        self.labels = labels
        self.name = name
        self.credentials = credentials
        self.TimePeriod = {"Start": start, "End": end}
        self.granularity = granularity
        self.request = 0
        self.request_success = 0
        self.request_error = 0
        self.refresh = refresh
        self.metrics = metrics
        # Billing is only available in the us-east region, so no reason to ask
        # for the region
        self.session = CostExplorerJob._make_session(self.credentials)

    @staticmethod
    def _make_session(credentials):
        try:
            key_id, secret_id, session_token = credentials.load_credentials()
            client = boto3.client("ce",
                                  aws_access_key_id=key_id,
                                  aws_secret_key_id=secret_id,
                                  aws_session_token=session_token)
            return client
        except ValueError:
            return boto3.client("ce")

    def execute(self, queue):
        results = []
        print('im executed')
        token = None
        while True:
            if token:
                kwargs = {'NextPageToken': token}
            else:
                kwargs = {}
            try:
                data = self.session.get_cost_and_usage(
                    TimePeriod=self.TimePeriod,
                    Granularity=self.granularity,
                    Metrics=[self.metrics],
                    GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
                    **kwargs)
                results += data['ResultsByTime']
                token = data.get('NextPageToken')
                if not token:
                    break
            except Exception as e:
                print(e)
                self.request_error += 1
                break
            else:
                self.request_success += 1
        queue.put({
            'metric_labels': self.labels,
            'name': self.name,
            'error_request_count': self.request_error,
            'success_request_count': self.request_success,
            'response': results
        })
