# -*- coding:utf-8 -*-
import sys

import os
import re


class ConfigManager(object):
    """
    config manager, read env variable: default one and specific one,
    auto generate config file according to template file
    replace ${XX} by env variable
    also do the validation in case of env variable is ""
    """

    def __init__(self, env_default_file_path, env_specific_file_path):
        super(ConfigManager, self).__init__()
        self.env_config = {}
        self.load = False
        self.env_default_file_path = env_default_file_path
        self.env_specific_file_path = env_specific_file_path

    def init_env_config(self):
        """
        first load default config and then load specific config
        """
        self.env_config.clear()
        self.read_config(self.env_default_file_path)
        self.read_config(self.env_specific_file_path)
        self.validate_config()
        self.load = True

    def read_config(self, file_path):
        """
        读取配置文件信息
        """
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                # annotation pass
                if line.startswith("#"):
                    continue
                items = line.strip().split("=")
                item_key = items[0].strip()
                item_value = items[1].strip()
                self.env_config[item_key] = item_value

    def validate_config(self):
        """
        env_config value can not be empty string(in case forget to assign value)
        """
        for key, value in self.env_config.items():
            assert value != ""

    def render_config_file(self, template_file_path, out_file_path):
        """
        replace template ${xx} with env variable xx, then generate new config file
        """
        if not self.load:
            self.init_env_config()

        pattern = re.compile(r'\${(\w+)}')
        data = []
        with open(template_file_path) as f:
            for line in f.readlines():
                new_line = pattern.sub(self.replace_func, line)
                data.append(new_line)

        with open(out_file_path, 'w') as f:
            f.write("".join(data))

    def replace_func(self, match):
        """
        replace ${var} with env variable
        """
        value = match.group(1)
        return self.env_config.get(value, None)

    def __getitem__(self, item):
        """
        interface to get env variable
        """
        if not self.load:
            self.init_env_config()
            self.load = True

        return self.env_config[item]


def auto_generate_config(conf_dir, config_dir, specific_env_mark=None, default_config_mark="default",
                         template_mark="template"):
    """
    :parameter conf_dir: conf_dir
    :parameter config_dir: env_config_dir
    :parameter specific_env_mark: env_mark
    :parameter default_config_mark: default_env_mark
    :parameter template_mark: template_mark
    """
    config_file_list = os.listdir(config_dir)
    default_config_file_name = None

    # fetch default config
    for config_file_name in config_file_list:
        if default_config_mark in config_file_name:
            default_config_file_name = config_file_name
            break

    # need default settings
    assert default_config_file_name is not None

    for config_file_name in config_file_list:
        if default_config_mark in config_file_name:
            continue
        env_name = config_file_name.split(".")[0]

        if specific_env_mark and specific_env_mark != env_name:
            continue

        config_manager = ConfigManager(os.path.join(config_dir, default_config_file_name),
                                       os.path.join(config_dir, config_file_name))
        config_dir_name = config_dir.split("/")[-1]
        conf_dir_list = os.listdir(conf_dir)
        for dir_name in conf_dir_list:
            if dir_name == config_dir_name:
                continue
            cur_dir = os.path.join(conf_dir, dir_name)
            cur_dir_file_list = os.listdir(cur_dir)
            for file_name in cur_dir_file_list:
                if template_mark in file_name:
                    config_manager.render_config_file(os.path.join(cur_dir, file_name),
                                                      os.path.join(cur_dir, file_name.replace(template_mark, env_name)))


if __name__ == "__main__":
    # auto generate specific batch config files: python config_manager.py conf conf/env [online]
    # auto generate all batch config files: python config_manager.py conf conf/env
    # python config_manager.py conf conf/env [online]
    base_dir = sys.argv[1]
    env_dir = sys.argv[2]
    # if not assign then generate all
    env_mark = sys.argv[3] if len(sys.argv) > 3 else None
    auto_generate_config(base_dir, env_dir, env_mark)
