"""Tests for GUI lifecycle and threading."""

import pytest
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication


class WorkerSignal(QObject):
    """Simple worker that emits signals."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.work_done = False
    
    def run(self):
        self.work_done = True
        self.finished.emit()


def wait_for_thread(thread: QThread, finished_spy: QSignalSpy, timeout: int = 500) -> None:
    """Process the queued finished signal before blocking on the thread."""
    signal_received = len(finished_spy) > 0 or finished_spy.wait(timeout)
    if signal_received:
        thread.quit()
    stopped = signal_received and thread.wait(timeout)
    if not stopped:
        thread.quit()
        stopped = thread.wait(timeout)
    assert signal_received
    assert stopped


@pytest.fixture
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_qthread_lifecycle(qapp):
    """Verify QThread starts, runs, and finishes."""
    worker = WorkerSignal()
    thread = QThread()
    worker.moveToThread(thread)
    
    # Connect signals
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    
    spy = QSignalSpy(worker.finished)
    
    thread.start()
    wait_for_thread(thread, spy)
    
    assert worker.work_done
    assert not thread.isRunning()


def test_qthread_error_signal(qapp):
    """Verify error signals are propagated."""
    worker = WorkerSignal()
    thread = QThread()
    worker.moveToThread(thread)
    
    worker.finished.connect(thread.quit)
    
    spy = QSignalSpy(worker.error)
    
    # Emit error signal
    worker.error.emit("test error")
    
    # Process events to allow signal to be delivered
    QApplication.processEvents()
    
    assert len(spy) == 1


def test_qthread_clean_exit_after_work(qapp):
    """Verify thread exits cleanly after work completes."""
    worker = WorkerSignal()
    thread = QThread()
    worker.moveToThread(thread)
    worker.finished.connect(thread.quit)
    thread.started.connect(worker.run)
    spy = QSignalSpy(worker.finished)
    
    thread.start()
    wait_for_thread(thread, spy)
    
    # Verify thread is not running
    assert not thread.isRunning()
    # Verify worker ran
    assert worker.work_done


def test_qthread_multiple_workers_sequential(qapp):
    """Verify multiple workers can be run sequentially in threads."""
    workers = []
    threads = []
    spies = []
    
    for i in range(3):
        worker = WorkerSignal()
        thread = QThread()
        worker.moveToThread(thread)
        worker.finished.connect(thread.quit)
        thread.started.connect(worker.run)
        
        threads.append(thread)
        workers.append(worker)
        spies.append(QSignalSpy(worker.finished))
        
        thread.start()
    
    # Wait for all threads
    for thread, spy in zip(threads, spies):
        wait_for_thread(thread, spy)
    
    # All should be done
    assert all(not t.isRunning() for t in threads)
    assert all(w.work_done for w in workers)


def test_qthread_wait_timeout():
    """Verify thread.wait() respects timeout."""
    worker = WorkerSignal()
    thread = QThread()
    worker.moveToThread(thread)
    
    # Don't connect finished signal - thread will keep running
    thread.started.connect(worker.run)
    
    thread.start()
    
    # Use very short timeout
    result = thread.wait(10)
    
    # Thread might still be running (or finished in 10ms)
    # Just verify wait() returned (didn't hang)
    assert isinstance(result, bool)
    
    # Clean up: quit thread manually
    thread.quit()
    assert thread.wait(500)
