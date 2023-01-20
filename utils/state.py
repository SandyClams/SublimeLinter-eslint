from sublime import set_timeout_async

def to_milliseconds(option = None):
  return int(option * 1000) if isinstance(option, float) else (
    option if isinstance(option, int) else 0
  )

class LintState:
  __instances = {}

  def __new__(cls, linter_instance):
    view_id = linter_instance.view.id()

    if view_id in cls.__instances:
      return cls.__instances[view_id]

    view_state = super(LintState, cls).__new__(cls)
    return view_state

  def __init__(self, linter_instance):
    view_id = linter_instance.view.id()

    if not view_id in type(self).__instances:
      self.id = view_id
      self.is_awaiting_async_update = False
      self.most_recent_fatal_result = None
      self.error_delay = to_milliseconds(linter_instance.settings.get('delay_fatal_errors_by'))
      # self.retain_delay = to_milliseconds(linter_instance.settings.get('retain_previous_errors_by'))
      self.retain_delay = 5000
      self.error_store = []
      self.fatal_store = []
      type(self).__instances[view_id] = self

  def add_fatal_result(self, is_async_update = False):
    self.is_awaiting_async_update = False

    if self.most_recent_fatal_result:
      self.fatal_store = [self.most_recent_fatal_result]

      if is_async_update:
        set_timeout_async(lambda: self.expire_error_store(), self.retain_delay)

  def expire_error_store(self):
    if self.fatal_store:
      self.error_store.clear()

  def get(self, name, default = None):
    return getattr(self, name, default)

  def get_aggregate_results(self):
    return self.error_store + self.fatal_store

  def process_fatal_result(self, fatal_result):
    self.most_recent_fatal_result = fatal_result

    if self.fatal_store:
      self.add_fatal_result()
    elif not self.is_awaiting_async_update:
      self.is_awaiting_async_update = True
      set_timeout_async(lambda: self.add_fatal_result(True), self.error_delay)

  def store_valid_results(self, lint_results):
    self.most_recent_fatal_result = None
    self.fatal_store = []
    self.error_store = lint_results
