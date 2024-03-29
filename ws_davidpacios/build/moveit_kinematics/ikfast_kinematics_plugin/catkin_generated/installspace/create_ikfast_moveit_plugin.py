#!/usr/bin/env python3

"""
IKFast Plugin Generator for MoveIt

Creates a kinematics plugin using the output of IKFast from OpenRAVE.
This plugin and the move_group node can be used as a general
kinematics service, from within the moveit planning environment, or in
your own ROS node.

Author: Dave Coleman, PickNik Robotics
        Michael Lautman, PickNik Robotics
        Based heavily on the arm_kinematic_tools package by Jeremy Zoss, SwRI
        and the arm_navigation plugin generator by David Butterworth, KAIST

Date: March 2013

"""
"""
Copyright (c) 2013, Jeremy Zoss, SwRI
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the Willow Garage, Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
IABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import re
import os
import yaml
from lxml import etree
from getpass import getuser
import shutil
import argparse

try:
    from roslib.packages import get_pkg_dir, InvalidROSPkgException
except ImportError:
    print("Failed to import roslib. No ROS environment available? Trying without.")
    # define stubs
    class InvalidROSPkgException(Exception):
        pass

    def get_pkg_dir(pkg_name):
        raise InvalidROSPkgException(f"Failed to locate ROS package {pkg_name}")


# Package containing this file
plugin_gen_pkg = "moveit_kinematics"
# Allowed search modes, see SEARCH_MODE enum in template file
search_modes = ["OPTIMIZE_MAX_JOINT", "OPTIMIZE_FREE_JOINT"]


def create_parser():
    parser = argparse.ArgumentParser(
        description="Generate an IKFast MoveIt kinematic plugin"
    )
    parser.add_argument("robot_name", help="The name of your robot")
    parser.add_argument(
        "planning_group_name",
        help="The name of the planning group for which your IKFast solution was generated",
    )
    parser.add_argument(
        "ikfast_plugin_pkg",
        help="The name of the MoveIt IKFast Kinematics Plugin to be created/updated",
    )
    parser.add_argument(
        "base_link_name",
        help="The name of the base link that was used when generating your IKFast solution",
    )
    parser.add_argument(
        "eef_link_name",
        help="The name of the end effector link that was used when generating your IKFast solution",
    )
    parser.add_argument(
        "ikfast_output_path",
        help="The full path to the analytic IK solution output by IKFast",
    )
    parser.add_argument(
        "--search_mode",
        default=search_modes[0],
        help="The search mode used to solve IK for robots with more than 6DOF",
    )
    parser.add_argument(
        "--srdf_filename", help="The name of your robot. Defaults to <robot_name>.srdf"
    )
    parser.add_argument(
        "--robot_name_in_srdf",
        help="The name of your robot as defined in the srdf. Defaults to <robot_name>",
    )
    parser.add_argument(
        "--moveit_config_pkg",
        help="The robot moveit_config package. Defaults to <robot_name>_moveit_config",
    )
    parser.add_argument(
        "--eef_direction",
        type=float,
        nargs=3,
        metavar=("X", "Y", "Z"),
        default=[0, 0, 1],
        help="The end effector's direction vector defined in its own frame, which is used to generate necessary parameters to a IKFast solver of one of the following types: Direction3D, Ray4D, TranslationDirection5D, Translation*AxisAngle4D, and Translation*AxisAngle*Norm4D. When not specified, a unit-z vector, i.e. 0 0 1, is adopted as default",
    )
    return parser


def populate_optional(args):
    if args.srdf_filename is None:
        args.srdf_filename = args.robot_name + ".srdf"
    if args.robot_name_in_srdf is None:
        args.robot_name_in_srdf = args.robot_name
    if args.moveit_config_pkg is None:
        args.moveit_config_pkg = args.robot_name + "_moveit_config"


def print_args(args):
    print("Creating IKFastKinematicsPlugin with parameters: ")
    print(f" robot_name:           {args.robot_name}")
    print(f" base_link_name:       {args.base_link_name}")
    print(f" eef_link_name:        {args.eef_link_name}")
    print(f" planning_group_name:  {args.planning_group_name}")
    print(f" ikfast_plugin_pkg:    {args.ikfast_plugin_pkg}")
    print(f" ikfast_output_path:   {args.ikfast_output_path}")
    print(f" search_mode:          {args.search_mode}")
    print(f" srdf_filename:        {args.srdf_filename}")
    print(f" robot_name_in_srdf:   {args.robot_name_in_srdf}")
    print(f" moveit_config_pkg:    {args.moveit_config_pkg}")
    print(
        f" eef_direction:        {args.eef_direction[0]:g} {args.eef_direction[1]:g} {args.eef_direction[2]:g}"
    )
    print("")


def update_deps(reqd_deps, req_type, e_parent):
    curr_deps = [e.text for e in e_parent.findall(req_type)]
    missing_deps = set(reqd_deps) - set(curr_deps)
    for dep in missing_deps:
        etree.SubElement(e_parent, req_type).text = dep


def validate_openrave_version(args):
    if not os.path.exists(args.ikfast_output_path):
        raise Exception("Can't find IKFast source code at " + args.ikfast_output_path)

    # Detect version of IKFast used to generate solver code
    solver_version = 0
    with open(args.ikfast_output_path, "r") as src:
        for line in src:
            if line.startswith("/// ikfast version"):
                line_search = re.search("ikfast version (.*) generated", line)
                if line_search:
                    solver_version = int(line_search.group(1), 0) & ~0x10000000
                break
    print(f"Found source code generated by IKFast version {solver_version}")

    # Chose template depending on IKFast version
    if solver_version >= 56:
        setattr(args, "template_version", 61)
    else:
        raise Exception("This converter requires IKFast 0.5.6 or newer.")


def xmlElement(name, text=None, **attributes):
    e = etree.Element(name, **attributes)
    e.text = text
    return e


def create_ikfast_package(args):
    try:
        setattr(args, "ikfast_plugin_pkg_path", get_pkg_dir(args.ikfast_plugin_pkg))
    except InvalidROSPkgException:
        args.ikfast_plugin_pkg_path = os.path.abspath(args.ikfast_plugin_pkg)
        print(
            f"Createing new package {args.ikfast_plugin_pkg} it in {args.ikfast_plugin_pkg_path}."
        )
        # update pkg name to basename of path
        args.ikfast_plugin_pkg = os.path.basename(args.ikfast_plugin_pkg_path)

    src_path = args.ikfast_plugin_pkg_path + "/src/"
    if not os.path.exists(src_path):
        os.makedirs(src_path)

    include_path = args.ikfast_plugin_pkg_path + "/include/"
    if not os.path.exists(include_path):
        os.makedirs(include_path)

    # Create package.xml
    pkg_xml_path = args.ikfast_plugin_pkg_path + "/package.xml"
    if not os.path.exists(pkg_xml_path):
        root = xmlElement("package", format="2")
        root.append(xmlElement("name", text=args.ikfast_plugin_pkg))
        root.append(xmlElement("version", text="0.0.0"))
        root.append(
            xmlElement("description", text="IKFast plugin for " + args.robot_name)
        )
        root.append(xmlElement("license", text="BSD"))
        user_name = getuser()
        root.append(
            xmlElement("maintainer", email=f"{user_name}@todo.todo", text=user_name)
        )
        root.append(xmlElement("buildtool_depend", text="catkin"))
        etree.ElementTree(root).write(
            pkg_xml_path, xml_declaration=True, pretty_print=True, encoding="UTF-8"
        )
        print(f"Created package.xml at: '{pkg_xml_path}'")


def find_template_dir():
    for candidate in [os.path.dirname(__file__) + "/../templates"]:
        if os.path.exists(candidate) and os.path.exists(candidate + "/ikfast.h"):
            return os.path.realpath(candidate)
    try:
        return os.path.join(
            get_pkg_dir(plugin_gen_pkg), "ikfast_kinematics_plugin/templates"
        )
    except InvalidROSPkgException:
        raise Exception(f"Can't find package {plugin_gen_pkg}")


def update_ikfast_package(args):
    # Copy the source code generated by IKFast into our src folder
    src_path = args.ikfast_plugin_pkg_path + "/src/"
    solver_file_path = (
        src_path
        + args.robot_name
        + "_"
        + args.planning_group_name
        + "_ikfast_solver.cpp"
    )
    if not os.path.exists(solver_file_path) or not os.path.samefile(
        args.ikfast_output_path, solver_file_path
    ):
        shutil.copy2(args.ikfast_output_path, solver_file_path)

    if not os.path.exists(solver_file_path):
        raise Exception(
            f"Failed to copy IKFast source code from '{args.ikfast_output_path}' to '{solver_file_path}'\n"
            "Manually copy the source file generated by IKFast to this location and re-run"
        )
    # Remember ikfast solver file for update of MoveIt package
    args.ikfast_output_path = solver_file_path

    # Get template folder location
    template_dir = find_template_dir()

    # namespace for the plugin
    setattr(args, "namespace", args.robot_name + "_" + args.planning_group_name)
    replacements = dict(
        _ROBOT_NAME_=args.robot_name,
        _GROUP_NAME_=args.planning_group_name,
        _SEARCH_MODE_=args.search_mode,
        _EEF_LINK_=args.eef_link_name,
        _BASE_LINK_=args.base_link_name,
        _PACKAGE_NAME_=args.ikfast_plugin_pkg,
        _NAMESPACE_=args.namespace,
        _EEF_DIRECTION_=f"{args.eef_direction[0]:g}, {args.eef_direction[1]:g}, {args.eef_direction[2]:g}",
    )

    # Copy ikfast header file
    copy_file(
        template_dir + "/ikfast.h",
        args.ikfast_plugin_pkg_path + "/include/ikfast.h",
        "ikfast header file",
    )
    # Create ikfast plugin template
    copy_file(
        template_dir
        + "/ikfast"
        + str(args.template_version)
        + "_moveit_plugin_template.cpp",
        args.ikfast_plugin_pkg_path
        + "/src/"
        + args.robot_name
        + "_"
        + args.planning_group_name
        + "_ikfast_moveit_plugin.cpp",
        "ikfast plugin file",
        replacements,
    )

    # Create plugin definition .xml file
    ik_library_name = args.namespace + "_moveit_ikfast_plugin"
    plugin_def = etree.Element("library", path="lib/lib" + ik_library_name)
    setattr(args, "plugin_name", args.namespace + "/IKFastKinematicsPlugin")
    cl = etree.SubElement(
        plugin_def,
        "class",
        name=args.plugin_name,
        type=args.namespace + "::IKFastKinematicsPlugin",
        base_class_type="kinematics::KinematicsBase",
    )
    desc = etree.SubElement(cl, "description")
    desc.text = f"IKFast{args.template_version} plugin for closed-form kinematics of {args.robot_name} {args.planning_group_name}"

    # Write plugin definition to file
    plugin_file_name = ik_library_name + "_description.xml"
    plugin_file_path = args.ikfast_plugin_pkg_path + "/" + plugin_file_name
    etree.ElementTree(plugin_def).write(
        plugin_file_path, xml_declaration=True, pretty_print=True, encoding="UTF-8"
    )
    print(f"Created plugin definition at  '{plugin_file_path}'")

    # Create CMakeLists file
    replacements.update(dict(_LIBRARY_NAME_=ik_library_name))
    copy_file(
        template_dir + "/CMakeLists.txt",
        args.ikfast_plugin_pkg_path + "/CMakeLists.txt",
        "cmake file",
        replacements,
    )

    # Add plugin export to package manifest
    parser = etree.XMLParser(remove_blank_text=True)
    package_file_name = args.ikfast_plugin_pkg_path + "/package.xml"
    package_xml = etree.parse(package_file_name, parser).getroot()

    # Make sure at least all required dependencies are in the depends lists
    build_deps = [
        "liblapack-dev",
        "moveit_core",
        "pluginlib",
        "roscpp",
        "tf2_kdl",
        "tf2_eigen",
    ]
    run_deps = ["liblapack-dev", "moveit_core", "pluginlib", "roscpp"]

    update_deps(build_deps, "build_depend", package_xml)
    update_deps(run_deps, "exec_depend", package_xml)

    # Check that plugin definition file is in the export list
    new_export = etree.Element("moveit_core", plugin="${prefix}/" + plugin_file_name)

    export_element = package_xml.find("export")
    if export_element is None:
        export_element = etree.SubElement(package_xml, "export")

    found = False
    for el in export_element.findall("moveit_core"):
        found = etree.tostring(new_export) == etree.tostring(el)
        if found:
            break

    if not found:
        export_element.append(new_export)

    # Always write the package xml file, even if there are no changes, to ensure
    # proper encodings are used in the future (UTF-8)
    etree.ElementTree(package_xml).write(
        package_file_name, xml_declaration=True, pretty_print=True, encoding="UTF-8"
    )
    print(f"Wrote package.xml at  '{package_file_name}'")

    # Create a script for easily updating the plugin in the future in case the plugin needs to be updated
    easy_script_file_path = args.ikfast_plugin_pkg_path + "/update_ikfast_plugin.sh"
    with open(easy_script_file_path, "w") as f:
        f.write(
            "search_mode="
            + args.search_mode
            + "\n"
            + "srdf_filename="
            + args.srdf_filename
            + "\n"
            + "robot_name_in_srdf="
            + args.robot_name_in_srdf
            + "\n"
            + "moveit_config_pkg="
            + args.moveit_config_pkg
            + "\n"
            + "robot_name="
            + args.robot_name
            + "\n"
            + "planning_group_name="
            + args.planning_group_name
            + "\n"
            + "ikfast_plugin_pkg="
            + args.ikfast_plugin_pkg
            + "\n"
            + "base_link_name="
            + args.base_link_name
            + "\n"
            + "eef_link_name="
            + args.eef_link_name
            + "\n"
            + "ikfast_output_path="
            + args.ikfast_output_path
            + "\n"
            + "eef_direction="
            + f'"{args.eef_direction[0]:g} {args.eef_direction[1]:g} {args.eef_direction[2]:g}"'
            + "\n\n"
            + "rosrun moveit_kinematics create_ikfast_moveit_plugin.py\\\n"
            + "  --search_mode=$search_mode\\\n"
            + "  --srdf_filename=$srdf_filename\\\n"
            + "  --robot_name_in_srdf=$robot_name_in_srdf\\\n"
            + "  --moveit_config_pkg=$moveit_config_pkg\\\n"
            + "  --eef_direction $eef_direction\\\n"
            + "  $robot_name\\\n"
            + "  $planning_group_name\\\n"
            + "  $ikfast_plugin_pkg\\\n"
            + "  $base_link_name\\\n"
            + "  $eef_link_name\\\n"
            + "  $ikfast_output_path\n"
        )

    print(f"Created update plugin script at '{easy_script_file_path}'")


def update_moveit_package(args):
    try:
        moveit_config_pkg_path = get_pkg_dir(args.moveit_config_pkg)
    except InvalidROSPkgException:
        raise RuntimeError(f"Failed to find package: {args.moveit_config_pkg}")

    # SRDF sanity checks
    try:
        srdf_file_name = moveit_config_pkg_path + "/config/" + args.srdf_filename
        srdf = etree.parse(srdf_file_name).getroot()

        robot_name = srdf.get("name")
        if args.robot_name_in_srdf != robot_name:
            raise RuntimeWarning(
                f"Robot name in srdf ('{robot_name}') doesn't match expected name ('{args.robot_name_in_srdf}')"
            )

        groups = [g.get("name") for g in srdf.findall("group")]
        if args.planning_group_name not in groups:
            raise RuntimeWarning(
                f"Planning group '{args.planning_group_name}' not defined in the SRDF."
                " Available groups: \n" + ", ".join(groups)
            )

    except IOError:
        print(f"Failed to find SRDF file: {srdf_file_name}")
    except etree.XMLSyntaxError as err:
        print(f"Failed to parse xml in file: {srdf_file_name}\n{err.msg}")

    # Modify kinematics.yaml file
    kin_yaml_file_name = moveit_config_pkg_path + "/config/kinematics.yaml"
    with open(kin_yaml_file_name, "r") as f:
        kin_yaml_data = yaml.safe_load(f)

    try:
        kin_yaml_data[args.planning_group_name]["kinematics_solver"] = args.plugin_name
    except KeyError:
        # create new group entry
        print(
            f"Creating new planning group entry in kinematics.yaml for '{args.planning_group_name}'"
        )
        kin_yaml_data[args.planning_group_name] = dict(
            kinematics_solver=args.plugin_name
        )

    with open(kin_yaml_file_name, "w") as f:
        yaml.dump(kin_yaml_data, f, default_flow_style=False)

    print(f"Modified kinematics.yaml at '{kin_yaml_file_name}'")


def copy_file(src_path, dest_path, description, replacements=None):
    if not os.path.exists(src_path):
        raise Exception(f"Can't find {description} at '{src_path}'")

    if replacements is None:
        replacements = dict()

    with open(src_path, "r") as f:
        content = f.read()

    # replace templates
    for key, value in replacements.items():
        content = re.sub(key, value, content)

    with open(dest_path, "w") as f:
        f.write(content)
    print(f"Created {description} at '{dest_path}'")


def main():
    parser = create_parser()
    args = parser.parse_args()

    populate_optional(args)
    print_args(args)
    validate_openrave_version(args)
    create_ikfast_package(args)
    update_ikfast_package(args)
    try:
        update_moveit_package(args)
    except Exception as ex:
        print(
            f"""Failed to update MoveIt package:
{ex}
Update your kinematics.yaml manually to include the following configuration:
{args.planning_group_name}:
  kinematics_solver: {args.plugin_name}"""
        )


if __name__ == "__main__":
    main()
