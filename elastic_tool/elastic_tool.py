import json
import sys

import requests

HEADERS = {'Content-Type': 'application/json'}


class EsTool:
    def __init__(self):
        self.es = self.validate_connection('elasticsearch_url_here')
        self.cat = self.Cat(self.es)
        self.cluster = self.Cluster(self.es)
        self.document = self.Document(self.es)
        self.indices = self.Indices(self.es)
        self.snapshot = self.Snapshot(self.es)
        self.watcher = self.Watcher(self.es)

    def __add__(self, other):
        return str(self.es) + other

    @staticmethod
    def validate_connection(es_instance):
        """Attempts .ping() command on given es instance

        :param str es_instance: ElasticSearch instance url to validate connection
        :return: Connection validated
        :rtype: str
        :raises: ConnectionError
        """
        es = requests.get(es_instance)
        if es.ok:
            return es_instance
        raise ConnectionError

    class Cat:
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html

        Because of the nature of the return values from the cat API, the methods here will print the output to the
        console directly, with nothing returned. You could print the method return value, but it achieves nothing.
        """

        def __init__(self, es):
            self.es = es

        def aliases(self, verbose=False, return_format='text'):
            """Returns health of elasticsearch cluster
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/aliases?{verbose}{return_format}&pretty", stream=True).text
                )

        @staticmethod
        def set_request_string(return_format, verbose):
            return_format = "format=" + return_format
            verbose = "v&" if verbose else ""
            return return_format, verbose

        def allocation(self, verbose=False, return_format='text'):
            """Returns health of elasticsearch cluster

            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/allocation?{verbose}{return_format}&pretty", stream=True).text
            )

        def anomaly_detectors(self, verbose=False, return_format='text'):
            """Returns configuration and usage information about anomaly detection jobs
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/anomaly_detectors?{verbose}{return_format}&pretty", stream=True).text
            )

        def count_all(self, verbose=False, return_format='text'):
            """Returns number of documents in every index
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/count?{verbose}{return_format}&pretty", stream=True).text
            )

        def count(self, index, verbose=False, return_format='text'):
            """Returns number of documents in index
            :param str index: Index to count
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/{index}/_count?{verbose}{return_format}&pretty", stream=True).text
            )

        def dataframe_analytics(self, verbose=False, return_format='text'):
            """Returns information about data frame analytics jobs.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/ml/data_frame/analytics?{verbose}{return_format}&pretty",
                             stream=True).text
            )

        def datafeeds(self, verbose=False, return_format='text'):
            """Returns information about data feeds.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/ml/datafeeds?{verbose}{return_format}&pretty", stream=True).text
            )

        def field_data_all(self, verbose=False, return_format='text'):
            """Returns information about field data.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/fielddata?{verbose}{return_format}&pretty", stream=True).text
            )

        def field_data(self, field, verbose=False, return_format='text'):
            """Returns information about field data.
            :param str field: Field to get information about
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/fielddata/{field}?{verbose}{return_format}&pretty", stream=True).text
            )

        def health(self, verbose=False, return_format='text'):
            """Returns health of elasticsearch cluster
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/health?{verbose}{return_format}&pretty", stream=True).text
            )

        def indices_all(self, verbose=False, return_format='text'):
            """Returns information about indices
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/indices?{verbose}{return_format}&pretty", stream=True).text
            )

        def indices(self, index, verbose=False, return_format='text'):
            """Returns information about index
            :param str index: Index to get information about
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/indices/{index}?{verbose}{return_format}&pretty", stream=True).text
            )

        def master(self, verbose=False, return_format='text'):
            """Returns information about the master node, including the ID, bound IP address, and name.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/master?{verbose}{return_format}&pretty", stream=True).text
            )

        def nodeattrs(self, verbose=False, return_format='text'):
            """Returns information about the node attributes.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/nodeattrs?{verbose}{return_format}&pretty", stream=True).text
            )

        def nodes(self, verbose=False, return_format='text'):
            """Returns information about the nodes.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/nodes?{verbose}{return_format}&pretty", stream=True).text
            )

        def pending_tasks(self, verbose=False, return_format='text'):
            """Returns information about the pending tasks.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/pending_tasks?{verbose}{return_format}&pretty", stream=True).text
            )

        def plugins(self, verbose=False, return_format='text'):
            """Returns information about the plugins.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/plugins?{verbose}{return_format}&pretty", stream=True).text
            )

        def recovery(self, verbose=False, return_format='text'):
            """Returns information about ongoing and completed shard recoveries
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/recovery?{verbose}{return_format}&pretty", stream=True).text
                )

        def repositories(self, verbose=False, return_format='text'):
            """Returns information about the repositories.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/repositories?{verbose}{return_format}&pretty", stream=True).text
                )

        def shards(self, verbose=False, return_format='text'):
            """Returns information about the shards.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/shards?{verbose}{return_format}&pretty", stream=True).text
                )

        def snapshots(self, repository, verbose=False, return_format='text'):
            """Returns information about the snapshots.
            :param str repository: Name of the repository the snapshots belong to
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/snapshots/{repository}?{verbose}{return_format}&pretty", stream=True).text
                )

        def tasks(self, verbose=False, return_format='text'):
            """Returns information about the tasks.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/tasks?{verbose}{return_format}&pretty", stream=True).text
                )

        def templates(self, verbose=False, return_format='text'):
            """Returns information about the templates.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/templates?{verbose}{return_format}&pretty", stream=True).text
                )

        def thread_pool(self, verbose=False, return_format='text'):
            """Returns information about the thread pool.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/thread_pool?{verbose}{return_format}&pretty", stream=True).text
                )

        def transforms(self, verbose=False, return_format='text'):
            """Returns information about the transforms.
            :param bool verbose: Verbose output
            :param str return_format: Format of output (text, json)
            """
            return_format, verbose = self.set_request_string(return_format, verbose)
            sys.stdout.write(
                requests.get(f"{self.es}/_cat/transforms?{verbose}{return_format}&pretty", stream=True).text
                )

    class Cluster:
        def __init__(self, es_instance):
            """
            :type es_instance: Elasticsearch
            """
            self.es = es_instance
            self.nodes = self.Nodes(self.es)
            self.tasks = self.Task(self.es)

        def explain_shard_allocation(self):
            """Provides an explanation for a shard’s current allocation.
            If the Elasticsearch security features are enabled,
            you must have the monitor or manage cluster privilege to use this API.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/allocation/explain").text)

        def health(self):
            """Returns the health status of a cluster.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/health").text)

        def pending_tasks(self):
            """Returns cluster-level changes that have not yet been executed.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/pending_tasks").text)

        def remote_info(self):
            """Returns configured remote cluster information

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/remote_info").text)

        def settings(self):
            """
            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/settings").text)

        def state(self, **kwargs):
            """
                Takes an optional keyword arg: 'metric': eg: instance.state(metric='nodes').
                If not specified, returns all metrics.
                    _all: Shows all metrics.
                    blocks: Shows the blocks part of the response.
                    master_node: Shows the master_node part of the response.
                    metadata: Shows the metadata part of the response. If you supply a comma separated list of indices,
                              the returned output will only contain metadata for these indices.
                    nodes:Shows the nodes part of the response.
                    routing_nodes: Shows the routing_nodes part of the response.
                    routing_table: Shows the routing_table part of the response. If you supply a comma separated list of
                                   indices, the returned output will only contain the routing table for these indices.
                    version: Shows the cluster state version.
            :return: API response data
            :rtype: dict
            """
            if 'metric' in kwargs and kwargs['metric'] in [
                'nodes', 'routing_table', 'routing_nodes', 'metadata', 'master_node', '_all', 'blocks', 'version'
            ]:
                return json.loads(requests.get(self.es + "/_cluster/state/" + kwargs['metric']).text)
            return json.loads(requests.get(self.es + "/_cluster/state").text)

        def stats(self):
            """The Cluster Stats API allows retrieving statistics from a cluster wide perspective.
             The API returns basic index metrics (shard numbers, store size, memory usage)
            and information about the current nodes that form the cluster
             (number, roles, os, jvm versions, memory usage, cpu and installed plugins).

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_cluster/stats").text)

        def info(self):
            """
            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_xpack").text)

        def usage(self):
            """
            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/_xpack/usage").text)

        class Nodes:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance
                self.shutdown = self.Shutdown(es_instance)

            def usage(self):
                """Returns information on the usage of features.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_nodes/usage").text)

            def hot_threads(self):
                """Returns the hot threads on each selected node in the cluster.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_nodes/hot_threads").text)

            def info(self):
                """Returns information about nodes in the cluster.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_nodes/").text)

            def stats(self):
                """Returns statistics about nodes in the cluster.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_nodes/stats").text)

            def desired(self):
                """Returns desired nodes info.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_nodes/desired_nodes/_latest").text)

            class Shutdown:
                def __init__(self, es_instance):
                    """
                    :type es_instance: Elasticsearch
                    """
                    self.es = es_instance

                def start(self, **kwargs):
                    """Starts a shutdown process on the node.
                    https://www.elastic.co/guide/en/elasticsearch/reference/current/put-shutdown.html

                    :return: API response data
                    :rtype: dict
                    """
                    return json.loads(requests.get(
                        self.es + f"/_nodes/{kwargs['node_id']}/shutdown",
                        headers=HEADERS,
                        data=kwargs['data']
                        ).text)

                def cancel(self, **kwargs):
                    """Cancels a shutdown process on the node.
                    https://www.elastic.co/guide/en/elasticsearch/reference/current/put-shutdown.html

                    :return: API response data
                    :rtype: dict
                    """
                    return json.loads(requests.get(
                        self.es + f"/_nodes/{kwargs['node_id']}/shutdown",
                        headers=HEADERS,
                        ).text)

                def status_all(self):
                    """Returns the shutdown status of all nodes in the cluster.

                    :return: API response data
                    :rtype: dict
                    """
                    return json.loads(requests.get(self.es + "/_nodes/shutdown").text)

                def status(self, **kwargs):
                    """Returns the status of a shutdown process on the node.
                    https://www.elastic.co/guide/en/elasticsearch/reference/current/get-shutdown.html

                    :return: API response data
                    :rtype: dict
                    """
                    return json.loads(requests.get(
                        self.es + f"/_nodes/{kwargs['node_id']}/shutdown",
                        ).text)

        class Task:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance

            def list(self):
                """Returns information about the tasks currently executing in the cluster."""
                return json.loads(requests.get(self.es + "/_tasks").text)

    class Document:
        def __init__(self, es_instance):
            """
            :type es_instance: Elasticsearch
            """
            self.es = es_instance

        def create(self, **kwargs):
            """Creates a new document in the index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.post(self.es + "/" + kwargs['index'] + "/" + kwargs['type'] + "/",
                                            headers=HEADERS,
                                            data=json.dumps(kwargs['data'])).text)

        def get(self, index, doc_type, doc_id):
            """Returns a document.
            """
            return json.loads(requests.get(self.es + "/" + index + "/" + doc_type + "/" + doc_id).text)

        def multi_get(self, index, doc_type, ids: list):
            """Returns multiple documents.
            """
            return json.loads(requests.get(self.es + "/" + index + "/" + doc_type + "/_mget",
                                           headers=HEADERS,
                                           data=json.dumps({"ids": ids})).text)

        def update(self, **kwargs):
            """Updates a document.
            https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html"""
            return json.loads(requests.post(self.es + "/" + kwargs['index'] + "/" + kwargs['type'] + "/" + kwargs['id'],
                                            headers=HEADERS,
                                            data=json.dumps(kwargs['data'])).text)

        def bulk(self, **kwargs):
            """Creates or updates multiple documents at once.
            ! Bulked data has a very specific structure, that needs to be adhered to.
            See the Elasticsearch docs for more information.
            https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html"""
            return json.loads(requests.post(self.es + "/_bulk",
                                            headers=HEADERS,
                                            data=json.dumps(kwargs['data'])).text)

        def reindex(self, **kwargs):
            """Reindexes a document.
            https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html
            {
              "source": {
                "index": "my-index-000001"
              },
              "dest": {
                "index": "my-new-index-000001"
              }
            }"""
            return json.loads(requests.post(self.es + "/_reindex",
                                            headers=HEADERS,
                                            data=json.dumps(kwargs['data'])).text)

    class Indices:
        def __init__(self, es_instance):
            """
            :type es_instance: Elasticsearch
            """
            self.es = es_instance
            self.alias = self.Alias(self.es)
            self.cache = self.Cache(self.es)
            self.dangling = self.Dangling(self.es)

        def get(self, **kwargs):
            """Returns information about one or more indices.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/" + kwargs['index']).text)

        def create(self, data=None, **kwargs):
            """Creates a new index.

            :return: API response data
            :rtype: dict
            """
            if data is None:
                return json.loads(requests.put(self.es + "/" + kwargs['index']).text)
            return json.loads(requests.put(self.es + "/" + kwargs['index'], data=data).text)

        def delete(self, **kwargs):
            """Deletes an index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.delete(self.es + "/" + kwargs['index']).text)

        def exists(self, **kwargs):
            """Returns information about whether a particular index exists.

            :return: API response data
            :rtype: bool
            """
            return requests.head(self.es + "/" + kwargs['index']).status_code == 200

        def stats(self, **kwargs):
            """Returns statistics about one or more indices.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/" + kwargs['index'] + "/_stats").text)

        def segments(self, **kwargs):
            """Returns information about the segments in the index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/" + kwargs['index'] + "/_segments").text)

        def recovery(self, **kwargs):
            """Returns information about the recovery status of the index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(self.es + "/" + kwargs['index'] + "/_recovery").text)

        def clone(self, **kwargs):
            """Clones an index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.put(self.es + "/" + kwargs['index'] + "/_clone" + kwargs['clone_index']).text)

        def close(self, **kwargs):
            """Closes an index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.post(self.es + "/" + kwargs['index'] + "/_close").text)

        class Alias:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance

            def exists(self, **kwargs):
                """Returns information about whether a particular alias exists.

                :return: API response data
                :rtype: dict
                """
                return requests.head(self.es + "/" + kwargs['alias']).status_code == 200

            def get(self, **kwargs):
                """Retrieves information for one or more aliases.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_alias/" + kwargs['alias']).text)

            def create(self, **kwargs):
                """Creates a new alias for an index

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.put(self.es + kwargs['index'] + "/_alias/" + kwargs['alias']).text)

            def delete(self, **kwargs):
                """Deletes an alias.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.delete(self.es + kwargs['index'] + "/_alias/" + kwargs['alias']).text)

        class Cache:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance

            def clear(self, **kwargs):
                """Clears the cache for one or more indices.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.post(self.es + "/" + kwargs['index'] + "/_cache/clear").text)

        class Dangling:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance

            def list(self):
                """Retrieves information about dangling indices.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_dangling").text)

            def delete(self, **kwargs):
                """Deletes dangling indices.

                :return: API response data
                :rtype: dict
                """
                return json.loads(
                    requests.delete(self.es + "/_dangling" + kwargs['index_uuid'] + "?accept_data_loss=true").text)

    class Snapshot:
        def __init__(self, es_instance):
            """
            :type es_instance: Elasticsearch
            """
            self.es = es_instance
            self.repository = self.Repository(self.es)

        def create(self, **kwargs):
            """Creates a snapshot of an index.

            :return: API response data
            :rtype: dict
            """
            return json.loads(
                requests.put(f"{self.es}/_snapshot/{kwargs['repository_name']}/{kwargs['snapshot_name']}").text)

        def restore(self, **kwargs):
            """Restores a snapshot.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.post(
                f"{self.es}/_snapshot/{kwargs['repository_name']}/{kwargs['snapshot_name']}/_restore").text)

        def delete(self, **kwargs):
            """Deletes a snapshot.

            :return: API response data
            :rtype: dict
            """
            return json.loads(
                requests.delete(f"{self.es}/_snapshot/{kwargs['repository_name']}/{kwargs['snapshot_name']}").text)

        def status(self):
            """Retrieves the status of a snapshot.

            :return: API response data
            :rtype: dict
            """
            return json.loads(requests.get(f"{self.es}/_snapshot/_status").text)

        class Repository:
            def __init__(self, es_instance):
                """
                :type es_instance: Elasticsearch
                """
                self.es = es_instance

            def create(self, **kwargs):
                """Creates a repository.

                :return: API response data
                :rtype: dict
                """
                return json.loads(
                    requests.post(self.es + "/_snapshot/" + kwargs['repository_name'], json=kwargs['data'],
                                  headers=HEADERS).text)

            def get(self, **kwargs):
                """Retrieves information about a repository.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.get(self.es + "/_snapshot/" + kwargs['repository_name']).text)

            def delete(self, **kwargs):
                """Deletes a repository.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.delete(self.es + "/_snapshot/" + kwargs['repository_name']).text)

            def verify(self, **kwargs):
                """Verifies a repository.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.post(self.es + "/_snapshot/" + kwargs['repository_name'] + "/_verify").text)

            def cleanup(self, **kwargs):
                """Removes unused snapshots.

                :return: API response data
                :rtype: dict
                """
                return json.loads(
                    requests.delete(self.es + "/_snapshot/" + kwargs['repository_name'] + "/_cleanup").text)

            def analysis(self, **kwargs):
                """Returns the analysis of the specified index.

                :return: API response data
                :rtype: dict
                """
                return json.loads(requests.post(f"{self.es}/_snapshot/{kwargs['repository_name']}/_analyze").text)

    class Watcher:
        def __init__(self, es_instance):
            """
            :type es_instance: Elasticsearch
            """
            self.es = es_instance

        def stats(self, metric="_all"):
            """Returns the current Watcher stats.

            :return: API response data
            :rtype: dict
            """
            if metric in ['_all', 'current_watches', 'queued_watches']:
                return json.loads(requests.get(self.es + f"/_watcher/stats/{metric}").text)
            return json.loads(requests.get(self.es + f"/_watcher/stats").text)


# sean = EsTool('http://rest-acc3-susi-elasticsearch.ocpcmas.dcp.fi.eu.xdn.ericsson.se')
# print(sean.cat.indices_all(verbose=True))