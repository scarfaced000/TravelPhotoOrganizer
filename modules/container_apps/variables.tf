variable "resource_group_name" {
  description = "Resource Group 이름"
  type        = string
}

variable "location" {
  description = "Azure 리전"
  type        = string
}

variable "environment_name" {
  description = "Container Apps Environment 이름"
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "Log Analytics Workspace ID"
  type        = string
}

variable "container_app_name" {
  description = "Container App 이름"
  type        = string
}

variable "container_name" {
  description = "컨테이너 이름"
  type        = string
  default     = "main-container"
}

variable "container_image" {
  description = "컨테이너 이미지"
  type        = string
}

variable "container_cpu" {
  description = "컨테이너 CPU"
  type        = number
  default     = 0.5
}

variable "container_memory" {
  description = "컨테이너 메모리"
  type        = string
  default     = "1Gi"
}

variable "min_replicas" {
  description = "최소 레플리카 수"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "최대 레플리카 수"
  type        = number
  default     = 3
}

variable "ingress_external_enabled" {
  description = "외부 접근 허용"
  type        = bool
  default     = true
}

variable "ingress_target_port" {
  description = "컨테이너 포트"
  type        = number
  default     = 80
}

variable "environment_variables" {
  description = "환경 변수"
  type        = map(string)
  default     = {}
}

variable "secret_environment_variables" {
  description = "Secret 환경 변수"
  type        = map(string)
  default     = {}
}

variable "secrets" {
  description = "Container App Secrets"
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "registry_server" {
  description = "Container Registry 서버"
  type        = string
  default     = ""
}

variable "registry_username" {
  description = "Container Registry 사용자명"
  type        = string
  default     = ""
  sensitive   = true
}

variable "registry_password_secret_name" {
  description = "Registry 비밀번호 Secret 이름"
  type        = string
  default     = ""
}

variable "tags" {
  description = "리소스 태그"
  type        = map(string)
  default     = {}
}
