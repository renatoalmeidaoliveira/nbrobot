from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

menu = PluginMenu(
    label="Robot Framework",
    icon_class="mdi mdi-robot",
    groups=(
        (
            "Projects",
            (
                PluginMenuItem(
                    permissions=["nb_robot.view_project"],
                    link="plugins:nb_robot:project_list",
                    link_text="Projects",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_robot:project_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            permissions=["nb_robot.add_project"],
                        ),
                    ),
                ),
                PluginMenuItem(
                    permissions=["nb_robot.view_resource"],
                    link="plugins:nb_robot:resource_list",
                    link_text="Resources",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_robot:resource_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            permissions=["nb_robot.add_resource"],
                        ),
                    ),
                ),
                PluginMenuItem(
                    permissions=["nb_robot.view_variable"],
                    link="plugins:nb_robot:variable_list",
                    link_text="Variables",
                    buttons=(
                        PluginMenuButton(
                            "plugins:nb_robot:variable_add",
                            "Add",
                            "mdi mdi-plus-thick",
                            permissions=["nb_robot.add_variable"],
                        ),
                    ),
                ),
            ),
        ),
        
    ),
)