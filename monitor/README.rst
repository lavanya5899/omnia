Monitor
==========

The monitor role sets up `Grafana <https://grafana.com/>`_ ,  `Prometheus <https://prometheus.io/>`_ and `Loki <https://grafana.com/oss/loki/>`_ as Kubernetes pods.

**Setting Up Monitoring**

1. To set up monitoring, enter all required variables in ``monitor/monitor_config.yml``.


+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Parameter                  | Details                                                                                                                                                                                                                                                      |
+============================+==============================================================================================================================================================================================================================================================+
| docker_username            | Username for Dockerhub account. This will be used for Docker login and a   kubernetes secret will be created and patched to service account in default   namespace.  This kubernetes secret can   be used to pull images from private repositories.          |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Optional              |                                                                                                                                                                                                                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| docker_password            | Password for Dockerhub account. This field is mandatory if   ``docker_username`` is provided.                                                                                                                                                                |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Optional              |                                                                                                                                                                                                                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| appliance_k8s_pod_net_cidr |  Kubernetes pod network CIDR for   appliance k8s network. Make sure this value does not overlap with any of the   host networks.                                                                                                                             |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Required              |      **Default values**: ``192.168.0.0/16``                                                                                                                                                                                                                  |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| grafana_username           | The username for grafana UI. The length of username should be at least 5   characters. The username must not contain -,\, ',"                                                                                                                                |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Required              |                                                                                                                                                                                                                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| grafana_password           | Password used for grafana UI. The length of the password should be at   least 5 characters. The password must not contain -,\, ',". Do not use   "admin" in this field.                                                                                      |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Required              |                                                                                                                                                                                                                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mount_location             | The path where the Grafana persistent volume will be mounted.  If telemetry is set up, all telemetry   related files will also be stored and both timescale and mysql databases will   be mounted to this location. '/' is mandatory at the end of the path. |
|      ``string``            |                                                                                                                                                                                                                                                              |
|      Required              |      **Default values**: ``/opt/omnia/telemetry``                                                                                                                                                                                                            |
+----------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. note::

    * After running ``monitor.yml``, the file ``input/monitor_config.yml`` will be encrypted. To edit the file, use ``ansible-vault edit monitor_config.yml --vault-password-file .monitor_vault_key``.

    * Rocky 8.7 is not compatible with the Kubernetes installed by ``monitor.yml`` due to known issues with cri-o. For more information, `click here <https://github.com/cri-o/cri-o/issues/6197>`_.

2. Run the playbook using the following command: ::

    cd monitor
    ansible-playbook monitor.yml

