# python_config_auto_generate
use python to auto generate config files by template files with different user defined env variables

    initial conf structure

    conf
        env
            default.config
            local.config
            test.config
            online.config
        rpc(has template file)
            config.template.ini
        supervisor(has template file)
            supervisord.template.conf
        settings(has no template file just ignore)
            a.txt
        uwsgi(has template file)
            uwsgi.template.xml

    step 1:
        write template file. use ${VAR_XX} to define env variable(refer to config.template.ini)

    step 2:
        write default config and specific config, assign value to env variable(make sure all variables are not "")

    setp 3:
        run the script with two ways:

    3.1 generate all config files
        python config_manager.py conf conf/env
        conf
            env
                default.config
                local.config
                test.config
                online.config
            rpc(has template file)
                config.local.ini(auto generate)
                config.test.ini(auto generate)
                config.online.ini(auto generate)
                config.template.ini
            supervisor(has template file)
                supervisord.local.conf(auto generate)
                supervisord.test.conf(auto generate)
                supervisord.online.conf(auto generate)
                supervisord.template.conf
            settings(has no template file just ignore)
                a.txt
            uwsgi(has template file)
                uwsgi.local.xml(auto generate)
                uwsgi.test.xml(auto generate)
                uwsgi.online.xml(auto generate)
                uwsgi.template.xml

    3.2 generate specific config files
        python config_manager.py conf conf/env online

        conf
            env
                default.config
                local.config
                test.config
                online.config
            rpc(has template file)
                config.online.ini(auto generate)
                config.template.ini
            supervisor(has template file)
                supervisord.online.conf(auto generate)
                supervisord.template.conf
            settings(has no template file just ignore)
                a.txt
            uwsgi(has template file)
                uwsgi.online.xml(auto generate)
                uwsgi.template.xml
