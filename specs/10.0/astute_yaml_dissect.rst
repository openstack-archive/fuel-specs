..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

============================================
Dissect astute.yaml file to be more granular
============================================

https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect


-------------------
Problem description
-------------------

Today we have an astute.yaml as a source of truth when gathering data for
puppet modules. This file has a complex structure, some sections of it can
be met several times. It contains all the data about current cluster and as a
result it leads to following problems:

  * This file generates from DB objects, so when there are many nodes in a
    cluster, it takes too much time to serialize all these entities to a file
  * Astute.yaml has complex structure with too loose logic which leads to badly
    written YAQL queries based on it
  * Some data in this file meets twice or more frequently, which breaks DRY
    principle


----------------
Proposed changes
----------------

Data which serialized from DB should be restructured to better fit current
demands. There are thoughts which we should be guided by for this
restructurization:

  * Common data for all nodes should be split from other data and serialized
    only once. It gives us acceleration when serialize initial data from DB
  * All the data met twice or more in serialized objects must be united in one
    place
  * Similar data sections should be aggregated to bigger sections

The implementation of this approach requires changes in the Fuel:

  * Puppet manifests should be changed accordingly to changed sections

  * Deployment tasks: should be adapted to new serialized data objects

  * Nailgun: serialization should be changed from one big monolithic call to
    separate calls for different sections. Also DB structure should be changed
    to optimize serialization calls

Data structure proposed from bird's-eye perspective:

   .. code-block:: yaml

      openstack_data:
        aodh:
          db_password: NP41tnX5SYw5bwmPJdhMAhZE
          user_password: 37pD2jDZ7iYugRhNmwBBCjrE
        ceilometer:
          db_password: 9E8q5ns1SA8YYuCjEn5lK4OB
          enabled: false
          metering_secret: RSDzuyOzla8T6CKsJxZLP3Qg
          user_password: bwCQvgRupDyIysiFxTUDWUNH
        cinder:
          db_password: dyEK7BtkpwRyvB4N061zN1O9
          fixed_key: 4796d1141f1c9bdd6bf353299bf3d4a80162fa86c3af81b762a8f2c305d92d97
          user_password: lfkhPvSXdVdw5hJnAIMfG8U8
        external_mongo:
          hosts_ip: ''
          mongo_db_name: ceilometer
          mongo_password: ceilometer
          mongo_replset: ''
          mongo_user: ceilometer
        glance:
          db_password: udm202Ba1KaLCaOdvDGndOZT
          image_cache_max_size: '9405726720'
          user_password: Dq6JxJPzjD79zDzEsTH41zXN
        glance_glare:
          user_password: GRHpPC4AU2Ag5c7VThxq8zVY
        heat:
          auth_encryption_key: 8db1b801fd6e7a9e7f98535a2d2527a0
          db_password: xPYsohLgad4uZ2S3WTSKTZCG
          enabled: true
          rabbit_password: SVG6KGWxBCUXsBVlJfPqpwvy
          user_password: aa34H82AS7ixoAhORvjuSg7b
        horizon:
          secret_key: c6eb527cdacd75d87a026182df2e1d386df02a4b7f15d76dc27510d0a31a906a
        ironic:
          db_password: lg73uTDVe6IzWPx2977SNi0W
          enabled: false
          swift_tempurl_key: MJJmfeMCs9NZAvspT6KebSRM
          user_password: wZUOsg8ZcPenr3ZVwR4Pfva6
        keystone:
          admin_token: PAy8PZ5BUl0hrTf3o6XQiFLZ
          db_password: tOXyxfiTdtOBRg1zZHOESiyb
        mongo:
          enabled: false
        murano:
          db_password: wjriBYvepJAAp32S84G9Ut8J
          enabled: false
          rabbit_password: oQCCukvDLL1CrsrOqLCFiWwJ
          user_password: 9tAB2Dvr7hb5xbIy4wbMEeWe
        murano-cfapi:
          db_password: DsIzjwHj2kRCCMo1bMd7d2qh
          enabled: false
          rabbit_password: Ii0ax8JZ5EGjtonZXIXpC8ce
          user_password: RitF5hMLdIUZinJzlFhtgAtE
        murano_settings:
          murano_glance_artifacts_plugin: true
          murano_repo_url: http://storage.apps.openstack.org/
        neutron_advanced_configuration:
          neutron_dvr: false
          neutron_l2_pop: false
          neutron_l3_ha: false
          neutron_qos: false
        nova:
          db_password: fhLct13RyfnmJlkfAmIEon8x
          state_path: /var/lib/nova
          user_password: vkjvbHDjNQeXzkQSP8LYTje1
          nova_quota: false
        neutron:
          enabled: true
          L2:
            base_mac: fa:16:3e:00:00:00
            phys_nets:
              physnet1:
                bridge: br-floating
                vlan_range: null
              physnet2:
                bridge: br-prv
                vlan_range: None:None
            segmentation_type: vlan
          L3:
            use_namespaces: true
          database:
            passwd: D2mcdTSnALsEANrSwxvHweSH
          default_floating_net: admin_floating_net
          default_private_net: admin_internal_net
          keystone:
            admin_password: wUQlx244Vx5BjTEpOw6VbP71
          metadata:
            metadata_proxy_shared_secret: bZYSr64RnGR2v8sTqCnIYzqV
          predefined_networks:
            admin_floating_net:
              L2:
                network_type: flat
                physnet: physnet1
                router_ext: true
                segment_id: null
              L3:
                enable_dhcp: false
                floating:
                - 10.109.3.128:10.109.3.254
                gateway: 10.109.3.1
                nameservers: []
                subnet: 10.109.3.0/24
              shared: false
              tenant: admin
            admin_internal_net:
              L2:
                network_type: vlan
                physnet: physnet2
                router_ext: false
                segment_id: null
              L3:
                enable_dhcp: true
                floating: null
                gateway: 192.168.0.1
                nameservers:
                - 8.8.4.4
                - 8.8.8.8
                subnet: 192.168.0.0/24
              shared: false
              tenant: admin
        sahara:
          db_password: t1p0IbU2a4aUOYRZdBOJumf2
          enabled: false
          user_password: OXP2qQvOKNz1SpME5q50sVDP
        swift:
          user_password: nMQUYfuuCBrUPzp0XmsM6ETz

      cluster_data:
        cluster:
          fuel_version: '9.1'
          id: 1
          mode: ha_compact
          name: test
          status: deployment
          configuration: {}
          kernel_params:
            kernel: console=tty0 net.ifnames=1 biosdevname=0 rootdelay=90 nomodeset
          libvirt_type: qemu
          master_ip: 10.109.0.2
          openstack_version: mitaka-9.0

        plugins: []

        deployment:
          access:
            email: admin@localhost
            password: admin
            tenant: admin
            user: admin
          auth_key: ''
          auto_assign_floating_ip: false
          base_syslog:
            syslog_port: '514'
            syslog_server: 10.109.0.2
          cgroups:
          corosync:
            group: 226.94.1.1
            port: '12000'
            verified: false
          external_dns:
            dns_list:
            - 10.109.0.1
          external_ntp:
            ntp_list:
            - 0.fuel.pool.ntp.org
            - 1.fuel.pool.ntp.org
            - 2.fuel.pool.ntp.org
          mp:
          - point: '1'
            weight: '1'
          - point: '2'
            weight: '2'
          mysql:
            root_password: xUYHra8XD8N3qCVvSNMLY9HH
            wsrep_password: 4IKaH00SetyKKAegSVX5fkIK
          operator_user:
            authkeys: ''
            homedir: /home/fueladmin
            name: fueladmin
            password: eug4pUIw9ENvvAd41S2iR71R
            sudo: 'ALL=(ALL) NOPASSWD: ALL'
          service_user:
            homedir: /var/lib/fuel
            name: fuel
            password: TVm2Rb9tXoaf7OhG31YUdl4W
            root_password: r00tme
            sudo: 'ALL=(ALL) NOPASSWD: ALL'
          public_network_assignment:
            assign_to_all_nodes: false
          public_ssl:
            cert_data: ''
            cert_source: self_signed
            horizon: false
            hostname: public.fuel.local
            services: false
          puppet:
            manifests: rsync://10.109.0.2:/puppet/mitaka-9.0/manifests/
            modules: rsync://10.109.0.2:/puppet/mitaka-9.0/modules/
          puppet_debug: true
          rabbit:
            password: AMrUGo6qB9FkLdyIgr6ZdMKI
          release:
            name: Mitaka on Ubuntu 14.04
            operating_system: Ubuntu
            version: mitaka-9.0
          repo_setup:
            installer_initrd:
              local: /var/www/nailgun/ubuntu/x86_64/images/initrd.gz
              remote_relative: dists/trusty/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/initrd.gz
            installer_kernel:
              local: /var/www/nailgun/ubuntu/x86_64/images/linux
              remote_relative: dists/trusty/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/linux
            repos:
            - name: ubuntu
              priority: null
              section: main universe multiverse
              suite: trusty
              type: deb
              uri: http://archive.ubuntu.com/ubuntu/
            - name: ubuntu-updates
              priority: null
              section: main universe multiverse
              suite: trusty-updates
              type: deb
              uri: http://archive.ubuntu.com/ubuntu/
            - name: ubuntu-security
              priority: null
              section: main universe multiverse
              suite: trusty-security
              type: deb
              uri: http://archive.ubuntu.com/ubuntu/
            - name: mos
              priority: 1050
              section: main restricted
              suite: mos9.0
              type: deb
              uri: http://10.109.0.2:8080/mitaka-9.0/ubuntu/x86_64
            - name: mos-updates
              priority: 1050
              section: main restricted
              suite: mos9.0-updates
              type: deb
              uri: http://mirror.fuel-infra.org/mos-repos/ubuntu/9.0/
            - name: mos-security
              priority: 1050
              section: main restricted
              suite: mos9.0-security
              type: deb
              uri: http://mirror.fuel-infra.org/mos-repos/ubuntu/9.0/
            - name: mos-holdback
              priority: 1100
              section: main restricted
              suite: mos9.0-holdback
              type: deb
              uri: http://mirror.fuel-infra.org/mos-repos/ubuntu/9.0/
            - name: Auxiliary
              priority: 1150
              section: main restricted
              suite: auxiliary
              type: deb
              uri: http://10.109.0.2:8080/mitaka-9.0/ubuntu/auxiliary
            - name: proposed
              priority: 1200
              section: main restricted
              suite: mos9.0-proposed
              type: deb
              uri: http://mirror.fuel-infra.org/mos-repos/ubuntu/snapshots/9.0-2016-09-17-040338/
          resume_guests_state_on_host_boot: true
          run_ping_checker: true
          syslog:
            syslog_port: '514'
            syslog_server: ''
            syslog_transport: tcp
          test_vm_image:
            container_format: bare
            disk_format: qcow2
            glance_properties: ''
            img_name: TestVM
            img_path: /usr/share/cirros-testvm/cirros-x86_64-disk.img
            min_ram: 64
            os_name: cirros
            public: 'true'
          use_vcenter: false
          vms_conf: []
          workloads_collector:
            create_user: false
            enabled: true
            password: 6Yb0uMc7ryVCEpOgX1C91vPa
            tenant: services
            username: fuel_stats_user

        provision:
          cobbler:
            profile: ubuntu_1404_x86_64
          provision:
            codename: trusty
            engine:
              master_ip: 10.109.0.2
              password: elEZjTWKE79piXA8jnDVs2JX
              url: http://10.109.0.2:80/cobbler_api
              username: cobbler
            hostname: node-1.test.domain.local
            image_data:
              /:
                container: gzip
                format: ext4
                uri: http://10.109.0.2:8080/targetimages/env_1_ubuntu_1404_amd64.img.gz
              /boot:
                container: gzip
                format: ext2
                uri: http://10.109.0.2:8080/targetimages/env_1_ubuntu_1404_amd64-boot.img.gz
            interfaces:
              enp0s3:
                dns_name: node-1.test.domain.local
                ip_address: 10.109.0.5
                mac_address: 64:c9:46:e2:4f:84
                netmask: 255.255.255.0
                static: '0'
              enp0s4:
                mac_address: 64:dd:86:1d:b6:06
                static: '0'
              enp0s5:
                mac_address: 64:9d:68:89:72:25
                static: '0'
              enp0s6:
                mac_address: 64:0d:82:97:4b:d4
                static: '0'
              enp0s7:
                mac_address: 64:2a:d9:96:a5:2b
                static: '0'
            interfaces_extra:
              enp0s3:
                onboot: 'yes'
                peerdns: 'no'
              enp0s4:
                onboot: 'no'
                peerdns: 'no'
              enp0s5:
                onboot: 'no'
                peerdns: 'no'
              enp0s6:
                onboot: 'no'
                peerdns: 'no'
              enp0s7:
                onboot: 'no'
                peerdns: 'no'
            kernel_options:
              netcfg/choose_interface: 64:c9:46:e2:4f:84
              udevrules: 64:c9:46:e2:4f:84_enp0s3,64:dd:86:1d:b6:06_enp0s4,64:9d:68:89:72:25_enp0s5,64:0d:82:97:4b:d4_enp0s6,64:2a:d9:96:a5:2b_enp0s7
            ks_meta:
              admin_net: 10.109.0.0/24
              auth_key: '""'
              authorized_keys:
              - '"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZ1KhEDusYvqD+X1VR3HhTHL5aq6YfZ30G0hz0Ai3LzNNpZM04fPwACP7YbZYrt4eM3Af8Oj3NZt+ZoinVjbD6QkYzyAvV+3cHL7nQwFJ2f6TiYm6EUGqTtINFTTh+HVnz0Iv3XbcM2UCwb+2rdEKiSmuml+UfEQ13HEAuHoUkcl7wn0TDWdQWbyUuC6KmRG7ZlV9To3YGBt+I/TzoAsnfksx4lCDCsk70qpgrZo0cxym5PsxgtqpGcftygPZ9zAzWIPnm0MksiWXpe7Nj/QHUvD10Z4TY2BSH4Y3vzvCDc3KSxnPeIRL1bzJBJ5g451IwED8wJ7NyARXMfudwSmSP
                root@nailgun.test.domain.local"'
              cloud_init_templates:
                boothook: boothook_fuel_9.0_ubuntu.jinja2
                cloud_config: cloud_config_fuel_9.0_ubuntu.jinja2
                meta_data: meta_data_fuel_9.0_ubuntu.jinja2
              gw: 10.109.0.1
              image_data:
                /:
                  container: gzip
                  format: ext4
                  uri: http://10.109.0.2:8080/targetimages/env_1_ubuntu_1404_amd64.img.gz
                /boot:
                  container: gzip
                  format: ext2
                  uri: http://10.109.0.2:8080/targetimages/env_1_ubuntu_1404_amd64-boot.img.gz
              install_log_2_syslog: 1
              mco_auto_setup: 1
              mco_connector: rabbitmq
              mco_enable: 1
              mco_host: 10.109.0.2
              mco_identity: 1
              mco_password: RM2GHz6ZSVfazbCNDY6owVKy
              mco_pskey: unset
              mco_user: mcollective
              mco_vhost: mcollective
              pm_data:
                ks_spaces:
                - bootable: true
                  extra:
                  - disk/by-id/virtio-941e0d9ababe43429607
                  free_space: 50380
                  id: vda
                  name: vda
                  size: 51200
                  type: disk
                  volumes:
                  - size: 300
                    type: boot
                  - file_system: ext2
                    mount: /boot
                    name: Boot
                    size: 200
                    type: raid
                  - size: 64
                    type: lvm_meta_pool
                  - lvm_meta_size: 64
                    size: 19520
                    type: pv
                    vg: os
                  - lvm_meta_size: 64
                    size: 10304
                    type: pv
                    vg: logs
                  - lvm_meta_size: 64
                    size: 20544
                    type: pv
                    vg: mysql
                  - lvm_meta_size: 64
                    size: 268
                    type: pv
                    vg: horizon
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: image
                - bootable: false
                  extra:
                  - disk/by-id/virtio-f064bb5138734feeaa44
                  free_space: 50380
                  id: vdb
                  name: vdb
                  size: 51200
                  type: disk
                  volumes:
                  - size: 300
                    type: boot
                  - file_system: ext2
                    mount: /boot
                    name: Boot
                    size: 200
                    type: raid
                  - size: 192
                    type: lvm_meta_pool
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: os
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: logs
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: mysql
                  - lvm_meta_size: 64
                    size: 11124
                    type: pv
                    vg: horizon
                  - lvm_meta_size: 64
                    size: 39384
                    type: pv
                    vg: image
                - bootable: false
                  extra:
                  - disk/by-id/virtio-29424316cd0c45779a34
                  free_space: 50380
                  id: vdc
                  name: vdc
                  size: 51200
                  type: disk
                  volumes:
                  - size: 300
                    type: boot
                  - file_system: ext2
                    mount: /boot
                    name: Boot
                    size: 200
                    type: raid
                  - size: 256
                    type: lvm_meta_pool
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: os
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: logs
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: mysql
                  - lvm_meta_size: 0
                    size: 0
                    type: pv
                    vg: horizon
                  - lvm_meta_size: 64
                    size: 50444
                    type: pv
                    vg: image
                - _allocate_size: min
                  id: os
                  label: Base System
                  min_size: 19456
                  type: vg
                  volumes:
                  - file_system: ext4
                    mount: /
                    name: root
                    size: 15360
                    type: lv
                  - file_system: swap
                    mount: swap
                    name: swap
                    size: 4096
                    type: lv
                - _allocate_size: min
                  id: logs
                  label: Logs
                  min_size: 10240
                  type: vg
                  volumes:
                  - file_system: ext4
                    mount: /var/log
                    name: log
                    size: 10240
                    type: lv
                - _allocate_size: all
                  id: image
                  label: Image Storage
                  min_size: 5120
                  type: vg
                  volumes:
                  - file_system: xfs
                    mount: /var/lib/glance
                    name: glance
                    size: 89700
                    type: lv
                - _allocate_size: min
                  id: mysql
                  label: Mysql Database
                  min_size: 20480
                  type: vg
                  volumes:
                  - file_system: ext4
                    mount: /var/lib/mysql
                    name: root
                    size: 20480
                    type: lv
                - _allocate_size: min
                  id: horizon
                  label: Horizon Temp Storage
                  min_size: 11264
                  type: vg
                  volumes:
                  - file_system: xfs
                    mount: /var/lib/horizon
                    name: horizontmp
                    size: 11264
                    type: lv
              puppet_auto_setup: 1
              puppet_enable: 0
              puppet_master: localhost
              timezone: Etc/UTC
              user_accounts:
              - homedir: /home/fueladmin
                name: fueladmin
                password: eug4pUIw9ENvvAd41S2iR71R
                ssh_keys:
                - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZ1KhEDusYvqD+X1VR3HhTHL5aq6YfZ30G0hz0Ai3LzNNpZM04fPwACP7YbZYrt4eM3Af8Oj3NZt+ZoinVjbD6QkYzyAvV+3cHL7nQwFJ2f6TiYm6EUGqTtINFTTh+HVnz0Iv3XbcM2UCwb+2rdEKiSmuml+UfEQ13HEAuHoUkcl7wn0TDWdQWbyUuC6KmRG7ZlV9To3YGBt+I/TzoAsnfksx4lCDCsk70qpgrZo0cxym5PsxgtqpGcftygPZ9zAzWIPnm0MksiWXpe7Nj/QHUvD10Z4TY2BSH4Y3vzvCDc3KSxnPeIRL1bzJBJ5g451IwED8wJ7NyARXMfudwSmSP
                  root@nailgun.test.domain.local
                sudo:
                - 'ALL=(ALL) NOPASSWD: ALL'
              - homedir: /var/lib/fuel
                name: fuel
                password: TVm2Rb9tXoaf7OhG31YUdl4W
                ssh_keys:
                - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZ1KhEDusYvqD+X1VR3HhTHL5aq6YfZ30G0hz0Ai3LzNNpZM04fPwACP7YbZYrt4eM3Af8Oj3NZt+ZoinVjbD6QkYzyAvV+3cHL7nQwFJ2f6TiYm6EUGqTtINFTTh+HVnz0Iv3XbcM2UCwb+2rdEKiSmuml+UfEQ13HEAuHoUkcl7wn0TDWdQWbyUuC6KmRG7ZlV9To3YGBt+I/TzoAsnfksx4lCDCsk70qpgrZo0cxym5PsxgtqpGcftygPZ9zAzWIPnm0MksiWXpe7Nj/QHUvD10Z4TY2BSH4Y3vzvCDc3KSxnPeIRL1bzJBJ5g451IwED8wJ7NyARXMfudwSmSP
                  root@nailgun.test.domain.local
                sudo:
                - 'ALL=(ALL) NOPASSWD: ALL'
              - homedir: /root
                name: root
                password: r00tme
                ssh_keys:
                - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZ1KhEDusYvqD+X1VR3HhTHL5aq6YfZ30G0hz0Ai3LzNNpZM04fPwACP7YbZYrt4eM3Af8Oj3NZt+ZoinVjbD6QkYzyAvV+3cHL7nQwFJ2f6TiYm6EUGqTtINFTTh+HVnz0Iv3XbcM2UCwb+2rdEKiSmuml+UfEQ13HEAuHoUkcl7wn0TDWdQWbyUuC6KmRG7ZlV9To3YGBt+I/TzoAsnfksx4lCDCsk70qpgrZo0cxym5PsxgtqpGcftygPZ9zAzWIPnm0MksiWXpe7Nj/QHUvD10Z4TY2BSH4Y3vzvCDc3KSxnPeIRL1bzJBJ5g451IwED8wJ7NyARXMfudwSmSP
                  root@nailgun.test.domain.local
            method: image
            name: node-1
            name_servers: '"10.109.0.2"'
            name_servers_search: '"test.domain.local"'
            netboot_enabled: '1'
            packages: 'acl\nanacron\nbridge-utils\nbsdmainutils'
            power_address: 10.109.0.5
            power_pass: /root/.ssh/bootstrap.rsa
            power_type: ssh
            power_user: root
            profile: ubuntu_1404_x86_64
            slave_name: node-1
            uid: '1'
          use_cow_images: true

        networking:
          network_roles:
            admin/pxe: 10.109.0.5
            aodh/api: 10.109.1.4
            ceilometer/api: 10.109.1.4
            ceph/public: 10.109.2.2
            ceph/radosgw: 10.109.3.4
            ceph/replication: 10.109.2.2
            cinder/api: 10.109.1.4
            cinder/iscsi: 10.109.2.2
            ex: 10.109.3.4
            fw-admin: 10.109.0.5
            glance/api: 10.109.1.4
            glance/glare: 10.109.1.4
            heat/api: 10.109.1.4
            horizon: 10.109.1.4
            ironic/api: 10.109.1.4
            keystone/api: 10.109.1.4
            management: 10.109.1.4
            mgmt/corosync: 10.109.1.4
            mgmt/database: 10.109.1.4
            mgmt/memcache: 10.109.1.4
            mgmt/messaging: 10.109.1.4
            mgmt/vip: 10.109.1.4
            mongo/db: 10.109.1.4
            murano/api: 10.109.1.4
            murano/cfapi: 10.109.1.4
            neutron/api: 10.109.1.4
            neutron/floating: null
            neutron/private: null
            nova/api: 10.109.1.4
            nova/migration: 10.109.1.4
            public/vip: 10.109.3.4
            sahara/api: 10.109.1.4
            storage: 10.109.2.2
            swift/api: 10.109.1.4
            swift/replication: 10.109.2.2
          vips:
            management:
              ipaddr: 10.109.1.3
              is_user_defined: false
              namespace: haproxy
              network_role: mgmt/vip
              node_roles:
              - controller
              - primary-controller
              vendor_specific: null
            public:
              ipaddr: 10.109.3.3
              is_user_defined: false
              namespace: haproxy
              network_role: public/vip
              node_roles:
              - controller
              - primary-controller
              vendor_specific: null
            vrouter:
              ipaddr: 10.109.1.2
              is_user_defined: false
              namespace: vrouter
              network_role: mgmt/vip
              node_roles:
              - controller
              - primary-controller
              vendor_specific: null
            vrouter_pub:
              ipaddr: 10.109.3.2
              is_user_defined: false
              namespace: vrouter
              network_role: public/vip
              node_roles:
              - controller
              - primary-controller
              vendor_specific:
                iptables_rules:
                  ns_start:
                  - iptables -t nat -A POSTROUTING -o <%INT%> -j MASQUERADE
                  ns_stop:
                  - iptables -t nat -D POSTROUTING -o <%INT%> -j MASQUERADE
          nodes:
          - fqdn: node-1.test.domain.local
            internal_address: 10.109.1.4
            internal_netmask: 255.255.255.0
            name: node-1
            public_address: 10.109.3.4
            public_netmask: 255.255.255.0
            role: primary-controller
            storage_address: 10.109.2.2
            storage_netmask: 255.255.255.0
            swift_zone: '1'
            uid: '1'
            user_node_name: Untitled (4f:84)

        storage:
          admin_key: AQBZ4N9XAAAAABAAoYhxyiUrN7l9aIjK8lTQPg==
          auth_s3_keystone_ceph: false
          bootstrap_osd_key: AQBZ4N9XAAAAABAAMOY9z3o4Q7UCmAuDnEotvg==
          ephemeral_ceph: false
          fsid: 77a3b347-8383-4b80-815f-1e4cb23737da
          images_ceph: false
          images_vcenter: false
          mon_key: AQBZ4N9XAAAAABAAF5xNT+hUOyzrdc1vE2H2aw==
          objects_ceph: false
          osd_pool_size: '3'
          per_pool_pg_nums:
            .rgw: 128
            backups: 128
            compute: 128
            default_pg_num: 128
            images: 128
            volumes: 128
          pg_num: 128
          radosgw_key: AQBZ4N9XAAAAABAApd/HGO08/pzHHXizVi7oaQ==
          volumes_block_device: false
          volumes_ceph: false
          volumes_lvm: true


      node_data:
        fqdn: node-1.test.domain.local
        name: node-1
        node_roles:
        - primary-controller
        nova_cpu_pinning_enabled: false
        nova_hugepages_enabled: false
        swift_zone: '1'
        uid: '1'
        user_node_name: Untitled (4f:84)
        network_scheme:
          endpoints:
            br-ex:
              IP:
              - 10.109.3.4/24
              gateway: 10.109.3.1
              vendor_specific:
                provider_gateway: 10.109.3.1
            br-floating:
              IP: none
            br-fw-admin:
              IP:
              - 10.109.0.5/24
              vendor_specific:
                provider_gateway: 10.109.0.1
            br-mgmt:
              IP:
              - 10.109.1.4/24
            br-prv:
              IP: none
            br-storage:
              IP:
              - 10.109.2.2/24
          interfaces:
            enp0s3:
              vendor_specific:
                bus_info: '0000:00:03.0'
                driver: e1000
            enp0s4:
              vendor_specific:
                bus_info: '0000:00:04.0'
                driver: e1000
            enp0s5:
              vendor_specific:
                bus_info: '0000:00:05.0'
                driver: e1000
            enp0s6:
              vendor_specific:
                bus_info: '0000:00:06.0'
                driver: e1000
            enp0s7:
              vendor_specific:
                bus_info: '0000:00:07.0'
                driver: e1000
          provider: lnx
          roles:
            admin/pxe: br-fw-admin
            aodh/api: br-mgmt
            ceilometer/api: br-mgmt
            ceph/public: br-storage
            ceph/radosgw: br-ex
            ceph/replication: br-storage
            cinder/api: br-mgmt
            cinder/iscsi: br-storage
            ex: br-ex
            fw-admin: br-fw-admin
            glance/api: br-mgmt
            glance/glare: br-mgmt
            heat/api: br-mgmt
            horizon: br-mgmt
            ironic/api: br-mgmt
            keystone/api: br-mgmt
            management: br-mgmt
            mgmt/corosync: br-mgmt
            mgmt/database: br-mgmt
            mgmt/memcache: br-mgmt
            mgmt/messaging: br-mgmt
            mgmt/vip: br-mgmt
            mongo/db: br-mgmt
            murano/api: br-mgmt
            murano/cfapi: br-mgmt
            neutron/api: br-mgmt
            neutron/floating: br-floating
            neutron/private: br-prv
            nova/api: br-mgmt
            nova/migration: br-mgmt
            public/vip: br-ex
            sahara/api: br-mgmt
            storage: br-storage
            swift/api: br-mgmt
            swift/replication: br-storage
          transformations:
          - action: add-br
            name: br-fw-admin
          - action: add-br
            name: br-mgmt
          - action: add-br
            name: br-storage
          - action: add-br
            name: br-ex
          - action: add-br
            name: br-floating
            provider: ovs
          - action: add-patch
            bridges:
            - br-floating
            - br-ex
            mtu: 65000
            provider: ovs
          - action: add-br
            name: br-prv
            provider: ovs
          - action: add-patch
            bridges:
            - br-prv
            - br-fw-admin
            mtu: 65000
            provider: ovs
          - action: add-port
            bridge: br-fw-admin
            name: enp0s3
          - action: add-port
            bridge: br-ex
            name: enp0s4
          - action: add-port
            bridge: br-mgmt
            name: enp0s5
          - action: add-port
            bridge: br-storage
            name: enp0s6
          version: '1.1'
        node_volumes:
        - bootable: true
          extra:
          - disk/by-id/virtio-941e0d9ababe43429607
          free_space: 50380
          id: vda
          name: vda
          size: 51200
          type: disk
          volumes:
          - size: 300
            type: boot
          - file_system: ext2
            mount: /boot
            name: Boot
            size: 200
            type: raid
          - size: 64
            type: lvm_meta_pool
          - lvm_meta_size: 64
            size: 19520
            type: pv
            vg: os
          - lvm_meta_size: 64
            size: 10304
            type: pv
            vg: logs
          - lvm_meta_size: 64
            size: 20544
            type: pv
            vg: mysql
          - lvm_meta_size: 64
            size: 268
            type: pv
            vg: horizon
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: image
        - bootable: false
          extra:
          - disk/by-id/virtio-f064bb5138734feeaa44
          free_space: 50380
          id: vdb
          name: vdb
          size: 51200
          type: disk
          volumes:
          - size: 300
            type: boot
          - file_system: ext2
            mount: /boot
            name: Boot
            size: 200
            type: raid
          - size: 192
            type: lvm_meta_pool
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: os
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: logs
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: mysql
          - lvm_meta_size: 64
            size: 11124
            type: pv
            vg: horizon
          - lvm_meta_size: 64
            size: 39384
            type: pv
            vg: image
        - bootable: false
          extra:
          - disk/by-id/virtio-29424316cd0c45779a34
          free_space: 50380
          id: vdc
          name: vdc
          size: 51200
          type: disk
          volumes:
          - size: 300
            type: boot
          - file_system: ext2
            mount: /boot
            name: Boot
            size: 200
            type: raid
          - size: 256
            type: lvm_meta_pool
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: os
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: logs
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: mysql
          - lvm_meta_size: 0
            size: 0
            type: pv
            vg: horizon
          - lvm_meta_size: 64
            size: 50444
            type: pv
            vg: image
        - _allocate_size: min
          id: os
          label: Base System
          min_size: 19456
          type: vg
          volumes:
          - file_system: ext4
            mount: /
            name: root
            size: 15360
            type: lv
          - file_system: swap
            mount: swap
            name: swap
            size: 4096
            type: lv
        - _allocate_size: min
          id: logs
          label: Logs
          min_size: 10240
          type: vg
          volumes:
          - file_system: ext4
            mount: /var/log
            name: log
            size: 10240
            type: lv
        - _allocate_size: all
          id: image
          label: Image Storage
          min_size: 5120
          type: vg
          volumes:
          - file_system: xfs
            mount: /var/lib/glance
            name: glance
            size: 89700
            type: lv
        - _allocate_size: min
          id: mysql
          label: Mysql Database
          min_size: 20480
          type: vg
          volumes:
          - file_system: ext4
            mount: /var/lib/mysql
            name: root
            size: 20480
            type: lv
        - _allocate_size: min
          id: horizon
          label: Horizon Temp Storage
          min_size: 11264
          type: vg
          volumes:
          - file_system: xfs
            mount: /var/lib/horizon
            name: horizontmp
            size: 11264
            type: lv
        status: discover
        user_node_name: Untitled (4f:84)


Web UI
======

None


Nailgun
=======

* Nailgun should serialize common data only once for cluster and do it
  separately from other serialization tasks


Data model
----------

* DB structure should be changed to represent new structure


REST API
--------

None


Orchestration
=============

None


RPC Protocol
------------

None


Fuel Client
===========

None


Plugins
=======

Plugins for new releases should be rewritten according to the new astute.yaml
structure. Support of old astute.yaml structure will be dropped according to
global Fuel features deprecation policy.


Fuel Library
============

Puppet manifests uses hiera should be rewritten to use new data structure. The
same should be done with noop tests.


------------
Alternatives
------------

None


--------------
Upgrade impact
--------------

* Wrapper which will convert old DB structure to the new on upgrades should be
  written


---------------
Security impact
---------------

None


--------------------
Notifications impact
--------------------

None


---------------
End user impact
---------------

None


------------------
Performance impact
------------------

Performance for big clusters will be significantly improved (speed factor is
clearly depends on cluster size as common data grown based on nodes count).


-----------------
Deployment impact
-----------------

None


----------------
Developer impact
----------------

Plugins developers should implement new plugins versions depending on new
data scheme.


---------------------
Infrastructure impact
---------------------

None


--------------------
Documentation impact
--------------------

None


--------------
Implementation
--------------

Assignee(s)
===========

Primary assignee:
  Stanislaw Bogatkin <sbogatkin@mirantis.com>

Other contributors:
  Bulat Gaifullin <bgaifullin@mirantis.com>

Mandatory design review:
  Vladimir Kuklin <vkuklin@mirantis.com>

QA engineer:
  Alexander Kurenyshev <akurenyshev@mirantis.com>


Work Items
==========

* Change Nailgun to serialize data according to new structure

* Create deployment tasks to copy data to target nodes

* Change fuel-library hiera hierarchy to consume new data

* Change fuel-library puppet modules accordingly

* Change fuel-noop-fixtures to reflect new data structure


Dependencies
============

None

-----------
Testing, QA
-----------

* Nailgun's unit and integration tests will be extended to test new feature.

* Fuel-library noop tests will be changed accordingly

* Fuel Client's unit and integration tests will be extended to test new feature.


Acceptance criteria
===================

* Deploy should be successfully ran without old astute.yaml file

* Fuel-library tests should be passed with new data structure


----------
References
----------

1. LP Blueprint https://blueprints.launchpad.net/fuel/+spec/astute-yaml-dissect
