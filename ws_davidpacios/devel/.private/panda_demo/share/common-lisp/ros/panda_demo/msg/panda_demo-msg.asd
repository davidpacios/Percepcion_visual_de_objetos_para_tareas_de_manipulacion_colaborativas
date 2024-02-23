
(cl:in-package :asdf)

(defsystem "panda_demo-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "GsAction" :depends-on ("_package_GsAction"))
    (:file "_package_GsAction" :depends-on ("_package"))
    (:file "GsActionFeedback" :depends-on ("_package_GsActionFeedback"))
    (:file "_package_GsActionFeedback" :depends-on ("_package"))
    (:file "GsActionGoal" :depends-on ("_package_GsActionGoal"))
    (:file "_package_GsActionGoal" :depends-on ("_package"))
    (:file "GsActionResult" :depends-on ("_package_GsActionResult"))
    (:file "_package_GsActionResult" :depends-on ("_package"))
    (:file "GsFeedback" :depends-on ("_package_GsFeedback"))
    (:file "_package_GsFeedback" :depends-on ("_package"))
    (:file "GsGoal" :depends-on ("_package_GsGoal"))
    (:file "_package_GsGoal" :depends-on ("_package"))
    (:file "GsResult" :depends-on ("_package_GsResult"))
    (:file "_package_GsResult" :depends-on ("_package"))
  ))