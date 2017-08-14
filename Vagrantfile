# -*- mode: ruby -*-
# vi: set ft=ruby :

# Main Vagrant Configuration for MongoSecurityPlaypen
Vagrant.configure(2) do |config|
    # Install Centos 7.3
    config.vm.box = "bento/centos-7.3"

    # Set higher timeout for waiting for each VM to come up
    config.vm.boot_timeout = 600

    # Workaround for Vagrant 1.8.5 bug, see: https://github.com/mitchellh/vagrant/issues/7610
    config.ssh.insert_key = false

    # CentrailIT VM
    config.vm.define :centralit do |centralit|
        centralit.vm.provider "virtualbox" do |vb|
            vb.name = "centralit"
            vb.memory = 512
            # Workaround for some VBox 5.x versions bug, see: https://github.com/chef/bento/issues/688
            vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
        end

        centralit.vm.hostname = "centralit.vagrant.dev"
        centralit.vm.network :private_network, ip: "192.168.14.100"

        centralit.vm.provision :ansible do |ansible|
            ansible.playbook = "centralit.yml"
        end
    end

    N = 3

    # Node VM x3
    (1..N).each do |i|
        # Create VMs in reverse order: 3rd, 2nd, 1st so can initiate further provisioning on 1st VM at end of cycle
        node = N + 1 - i

        config.vm.define "dbnode#{node}" do |server|
            server.vm.provider "virtualbox" do |vb|
                vb.name = "dbnode#{node}"
                vb.memory = 512
                # Workaround for some VBox 5.x versions bug, see: https://github.com/chef/bento/issues/688
                vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
            end

            server.vm.hostname = "dbnode#{node}.vagrant.dev"
            server.vm.network :private_network, ip: "192.168.14.10#{node}"

            server.vm.provision :ansible do |ansible|
                ansible.playbook = "dbnode.yml"
            end

            # Configure replica-set via mongod on 1st node
            if i == N
                server.vm.provision :ansible do |ansible|
                    ansible.playbook = "replicaset.yml"
                end
            end
        end
    end

    # Client VM
    config.vm.define :client do |client|
        client.vm.provider "virtualbox" do |vb|
            vb.name = "client"
            vb.memory = 512
            # Workaround for some VBox 5.x versions bug, see: https://github.com/chef/bento/issues/688
            vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
        end

        client.vm.hostname = "client.vagrant.dev"
        client.vm.network :private_network, ip: "192.168.14.109"

        client.vm.provision :ansible do |ansible|
            ansible.playbook = "client.yml"
        end
    end
=begin
ansible.verbose = "vvv"
=end
end

