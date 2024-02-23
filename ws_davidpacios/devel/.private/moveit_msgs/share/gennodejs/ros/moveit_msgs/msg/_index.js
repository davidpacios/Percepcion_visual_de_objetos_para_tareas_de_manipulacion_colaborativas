
"use strict";

let PlaceAction = require('./PlaceAction.js');
let MoveGroupActionGoal = require('./MoveGroupActionGoal.js');
let PickupAction = require('./PickupAction.js');
let MoveGroupActionFeedback = require('./MoveGroupActionFeedback.js');
let ExecuteTrajectoryResult = require('./ExecuteTrajectoryResult.js');
let PickupFeedback = require('./PickupFeedback.js');
let MoveGroupResult = require('./MoveGroupResult.js');
let MoveGroupSequenceAction = require('./MoveGroupSequenceAction.js');
let MoveGroupActionResult = require('./MoveGroupActionResult.js');
let PickupActionGoal = require('./PickupActionGoal.js');
let PlaceActionFeedback = require('./PlaceActionFeedback.js');
let PickupActionFeedback = require('./PickupActionFeedback.js');
let MoveGroupSequenceFeedback = require('./MoveGroupSequenceFeedback.js');
let ExecuteTrajectoryActionResult = require('./ExecuteTrajectoryActionResult.js');
let PickupResult = require('./PickupResult.js');
let PlaceActionResult = require('./PlaceActionResult.js');
let PlaceFeedback = require('./PlaceFeedback.js');
let MoveGroupSequenceResult = require('./MoveGroupSequenceResult.js');
let MoveGroupAction = require('./MoveGroupAction.js');
let PlaceGoal = require('./PlaceGoal.js');
let MoveGroupSequenceGoal = require('./MoveGroupSequenceGoal.js');
let PlaceResult = require('./PlaceResult.js');
let ExecuteTrajectoryAction = require('./ExecuteTrajectoryAction.js');
let ExecuteTrajectoryGoal = require('./ExecuteTrajectoryGoal.js');
let PickupActionResult = require('./PickupActionResult.js');
let MoveGroupSequenceActionFeedback = require('./MoveGroupSequenceActionFeedback.js');
let MoveGroupSequenceActionGoal = require('./MoveGroupSequenceActionGoal.js');
let PlaceActionGoal = require('./PlaceActionGoal.js');
let ExecuteTrajectoryActionGoal = require('./ExecuteTrajectoryActionGoal.js');
let MoveGroupGoal = require('./MoveGroupGoal.js');
let ExecuteTrajectoryFeedback = require('./ExecuteTrajectoryFeedback.js');
let ExecuteTrajectoryActionFeedback = require('./ExecuteTrajectoryActionFeedback.js');
let MoveGroupFeedback = require('./MoveGroupFeedback.js');
let PickupGoal = require('./PickupGoal.js');
let MoveGroupSequenceActionResult = require('./MoveGroupSequenceActionResult.js');
let DisplayTrajectory = require('./DisplayTrajectory.js');
let PositionIKRequest = require('./PositionIKRequest.js');
let PositionConstraint = require('./PositionConstraint.js');
let JointConstraint = require('./JointConstraint.js');
let CartesianTrajectory = require('./CartesianTrajectory.js');
let CartesianTrajectoryPoint = require('./CartesianTrajectoryPoint.js');
let TrajectoryConstraints = require('./TrajectoryConstraints.js');
let ConstraintEvalResult = require('./ConstraintEvalResult.js');
let GenericTrajectory = require('./GenericTrajectory.js');
let Grasp = require('./Grasp.js');
let RobotState = require('./RobotState.js');
let PlanningSceneComponents = require('./PlanningSceneComponents.js');
let CollisionObject = require('./CollisionObject.js');
let MotionSequenceItem = require('./MotionSequenceItem.js');
let Constraints = require('./Constraints.js');
let MotionSequenceResponse = require('./MotionSequenceResponse.js');
let MotionPlanDetailedResponse = require('./MotionPlanDetailedResponse.js');
let AttachedCollisionObject = require('./AttachedCollisionObject.js');
let OrientationConstraint = require('./OrientationConstraint.js');
let DisplayRobotState = require('./DisplayRobotState.js');
let PlanningScene = require('./PlanningScene.js');
let CostSource = require('./CostSource.js');
let ContactInformation = require('./ContactInformation.js');
let CartesianPoint = require('./CartesianPoint.js');
let JointLimits = require('./JointLimits.js');
let BoundingVolume = require('./BoundingVolume.js');
let VisibilityConstraint = require('./VisibilityConstraint.js');
let AllowedCollisionMatrix = require('./AllowedCollisionMatrix.js');
let KinematicSolverInfo = require('./KinematicSolverInfo.js');
let PlaceLocation = require('./PlaceLocation.js');
let WorkspaceParameters = require('./WorkspaceParameters.js');
let PlanningSceneWorld = require('./PlanningSceneWorld.js');
let MotionPlanRequest = require('./MotionPlanRequest.js');
let MotionPlanResponse = require('./MotionPlanResponse.js');
let GripperTranslation = require('./GripperTranslation.js');
let MoveItErrorCodes = require('./MoveItErrorCodes.js');
let PlannerParams = require('./PlannerParams.js');
let OrientedBoundingBox = require('./OrientedBoundingBox.js');
let LinkScale = require('./LinkScale.js');
let PlanningOptions = require('./PlanningOptions.js');
let LinkPadding = require('./LinkPadding.js');
let ObjectColor = require('./ObjectColor.js');
let RobotTrajectory = require('./RobotTrajectory.js');
let PlannerInterfaceDescription = require('./PlannerInterfaceDescription.js');
let MotionSequenceRequest = require('./MotionSequenceRequest.js');
let AllowedCollisionEntry = require('./AllowedCollisionEntry.js');

module.exports = {
  PlaceAction: PlaceAction,
  MoveGroupActionGoal: MoveGroupActionGoal,
  PickupAction: PickupAction,
  MoveGroupActionFeedback: MoveGroupActionFeedback,
  ExecuteTrajectoryResult: ExecuteTrajectoryResult,
  PickupFeedback: PickupFeedback,
  MoveGroupResult: MoveGroupResult,
  MoveGroupSequenceAction: MoveGroupSequenceAction,
  MoveGroupActionResult: MoveGroupActionResult,
  PickupActionGoal: PickupActionGoal,
  PlaceActionFeedback: PlaceActionFeedback,
  PickupActionFeedback: PickupActionFeedback,
  MoveGroupSequenceFeedback: MoveGroupSequenceFeedback,
  ExecuteTrajectoryActionResult: ExecuteTrajectoryActionResult,
  PickupResult: PickupResult,
  PlaceActionResult: PlaceActionResult,
  PlaceFeedback: PlaceFeedback,
  MoveGroupSequenceResult: MoveGroupSequenceResult,
  MoveGroupAction: MoveGroupAction,
  PlaceGoal: PlaceGoal,
  MoveGroupSequenceGoal: MoveGroupSequenceGoal,
  PlaceResult: PlaceResult,
  ExecuteTrajectoryAction: ExecuteTrajectoryAction,
  ExecuteTrajectoryGoal: ExecuteTrajectoryGoal,
  PickupActionResult: PickupActionResult,
  MoveGroupSequenceActionFeedback: MoveGroupSequenceActionFeedback,
  MoveGroupSequenceActionGoal: MoveGroupSequenceActionGoal,
  PlaceActionGoal: PlaceActionGoal,
  ExecuteTrajectoryActionGoal: ExecuteTrajectoryActionGoal,
  MoveGroupGoal: MoveGroupGoal,
  ExecuteTrajectoryFeedback: ExecuteTrajectoryFeedback,
  ExecuteTrajectoryActionFeedback: ExecuteTrajectoryActionFeedback,
  MoveGroupFeedback: MoveGroupFeedback,
  PickupGoal: PickupGoal,
  MoveGroupSequenceActionResult: MoveGroupSequenceActionResult,
  DisplayTrajectory: DisplayTrajectory,
  PositionIKRequest: PositionIKRequest,
  PositionConstraint: PositionConstraint,
  JointConstraint: JointConstraint,
  CartesianTrajectory: CartesianTrajectory,
  CartesianTrajectoryPoint: CartesianTrajectoryPoint,
  TrajectoryConstraints: TrajectoryConstraints,
  ConstraintEvalResult: ConstraintEvalResult,
  GenericTrajectory: GenericTrajectory,
  Grasp: Grasp,
  RobotState: RobotState,
  PlanningSceneComponents: PlanningSceneComponents,
  CollisionObject: CollisionObject,
  MotionSequenceItem: MotionSequenceItem,
  Constraints: Constraints,
  MotionSequenceResponse: MotionSequenceResponse,
  MotionPlanDetailedResponse: MotionPlanDetailedResponse,
  AttachedCollisionObject: AttachedCollisionObject,
  OrientationConstraint: OrientationConstraint,
  DisplayRobotState: DisplayRobotState,
  PlanningScene: PlanningScene,
  CostSource: CostSource,
  ContactInformation: ContactInformation,
  CartesianPoint: CartesianPoint,
  JointLimits: JointLimits,
  BoundingVolume: BoundingVolume,
  VisibilityConstraint: VisibilityConstraint,
  AllowedCollisionMatrix: AllowedCollisionMatrix,
  KinematicSolverInfo: KinematicSolverInfo,
  PlaceLocation: PlaceLocation,
  WorkspaceParameters: WorkspaceParameters,
  PlanningSceneWorld: PlanningSceneWorld,
  MotionPlanRequest: MotionPlanRequest,
  MotionPlanResponse: MotionPlanResponse,
  GripperTranslation: GripperTranslation,
  MoveItErrorCodes: MoveItErrorCodes,
  PlannerParams: PlannerParams,
  OrientedBoundingBox: OrientedBoundingBox,
  LinkScale: LinkScale,
  PlanningOptions: PlanningOptions,
  LinkPadding: LinkPadding,
  ObjectColor: ObjectColor,
  RobotTrajectory: RobotTrajectory,
  PlannerInterfaceDescription: PlannerInterfaceDescription,
  MotionSequenceRequest: MotionSequenceRequest,
  AllowedCollisionEntry: AllowedCollisionEntry,
};
